from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from ..models import Order, Cart
from ..serializers import OrderSerializer
from datetime import datetime
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
# Create your views here.

# Order CRUD View
class GetOrders(generics.ListAPIView):
    # Get Request (View Orders)
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        
        # --------------- ORDER QUERIES ---------------
        customer_id = self.request.query_params.get('customer_id', None)
        status = self.request.query_params.get('status', None)

        if customer_id is not None:
            queryset = queryset.filter(customer_id=customer_id)
        if status in ['Delivered', 'Failed to deliver']:
            queryset = queryset.filter(status=status)

        # --------------- SALES REPORT QUERIES ---------------

        # Gets the total numbers of orders Per Month
        getMonthOrders = self.request.query_params.get('getMonthOrders', None)

        if getMonthOrders is not None:
            months = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            month_number = months.get(getMonthOrders)

            if month_number is not None:
                queryset = queryset.filter(datetime__month=month_number).values()
        
        return queryset

class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming the order creation is successful
        order = serializer.save()

        # Update cart items with the created order ID
        cart_items = Cart.objects.filter(customer_id=request.data["customer_id"], order_id=None)
        total_amount = 0
        for cart_item in cart_items:
            total_amount += cart_item.total_amount * cart_item.quantity
            cart_item.order_id = order  # Assign the order object itself
            cart_item.save()

        # Additional custom logic if needed
        order = serializer.save(total_amount=total_amount) 

        headers = self.get_success_headers(serializer.data)
        message = "Order placed successfully."
        return Response({"message": message, "success": True, "order_id": order.id}, status=status.HTTP_201_CREATED, headers=headers)
    
class UpdateOrder(generics.RetrieveUpdateAPIView):
    # Get/Put Request (Modify Orders)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        status_before_update = instance.status

        self.perform_update(serializer)

        if status_before_update != "On the way" and instance.status == "On the way":
            # Send SMS Notification
            formatted_phone_number = "+63" + instance.phone_number[1:] 
            print("Sending SMS to " + formatted_phone_number)
            sendSMS(formatted_phone_number)
            print("Order status changed to 'On the way'.")
            
        success = True 
        message = "Order updated successfully." if success else "Failed to update order."
        
        return Response({"message": message, "success": success})

class DeleteOrder(generics.RetrieveDestroyAPIView):
    # Delete Request (Delete Orders)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            success = True 
            message = "Order deleted successfully."
            return Response({"message": message, "success": success}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            success = False
            message = f"Failed to delete order: {str(e)}"
            return Response({"message": message, "success": success}, status=status.HTTP_400_BAD_REQUEST)
    
    
def sendSMS(phone_number):
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body="Your order in CoffeeShop is already on the way, please prepare exact payment and expect delivery soon.", 
            from_=os.environ.get('TWILIO_NUMBER'),
            to=phone_number
        )
        print("Successfully sent SMS!")
        print(message.sid)
    except Exception as e:
        print(f"Failed to send SMS: {e}")
