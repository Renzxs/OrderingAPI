from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from ..models import Cart
from ..serializers import CartSerializer

# Cart CRUD View
class GetCart(generics.ListAPIView):
    # Get Request (View Cart)'
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = Cart.objects.all()

        # Get query parameters from the request
        customer_id = self.request.query_params.get('customer_id', None)

        # Filter queryset based on query parameters
        if customer_id is not None:
            queryset = queryset.filter(customer_id=customer_id)
            
        return queryset

class CreateCart(generics.CreateAPIView):
    # Post Request (Add to Cart)
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Check if the order was successfully created
        success = True  # Assuming the order creation is successful
        message = "Added to cart successfully." if success else "Failed to add to cart."
        
        return Response({"message": message, "success": success}, status=status.HTTP_201_CREATED, headers=headers)
    
class UpdateCart(generics.RetrieveUpdateAPIView):
    # Get/Put Request (Modify Cart)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Check if the order was successfully updated
        success = True  # Assuming the order update is successful
        message = "Cart updated successfully." if success else "Failed to update ."
        
        return Response({"message": message, "success": success})
    
class DeleteCart(generics.RetrieveDestroyAPIView):
    # Delete Request (Delete a Cart)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            success = True 
            message = "Cart item deleted successfully."
            return Response({"message": message, "success": success}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            success = False
            message = f"Failed to delete cart item: {str(e)}"
            return Response({"message": message, "success": success}, status=status.HTTP_400_BAD_REQUEST)