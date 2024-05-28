from rest_framework import serializers
from .models import Order, Cart, Customer, Rider, Product

# Order Modules Serializers
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", 
                  "customer_id", 
                #   "product_id",
                  "rider_id",
                  "payment_method",
                #   "quantity",
                  "total_amount",
                  "datetime",
                  "location_address",
                  "phone_number",
                  "method",
                  "status"]
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id",
                  "customer_id",
                  "product_id",
                  "quantity",
                  "total_amount",
                  "order_id"]
        
# Other Module Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", 
                  "customer_name",
                  "address"]
        
class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = ["id",
                  "rider_name"]
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id",
                  "product_name"]