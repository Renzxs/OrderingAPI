from django.db import models

# Create your models here.

# ------------- OTHER MODULES MODELS ----------------
class Customer(models.Model):
    # Customer Data Table
    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)

class Rider(models.Model):
    # Rider Data Table
    rider_name = models.CharField(max_length=100)

class Product(models.Model):
    # Product Data Table
    product_name = models.CharField(max_length=100)
     

# ------------- ORDER MODULE MODELS ----------------
class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    # product_id = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    rider_id = models.ForeignKey(Rider, on_delete=models.CASCADE, default=1, null=True)
    payment_method = models.CharField(max_length=50, null=True, default="") # Cash on Delivery, GCash & Bank Transfer (BPI, BPO)
    # quantity = models.IntegerField()
    total_amount = models.FloatField(null=True, default="")
    datetime = models.DateTimeField(auto_now_add=True)
    location_address = models.CharField(max_length=250, default="")
    phone_number = models.CharField(max_length=15, null=True)
    method = models.CharField(max_length=50, default="Delivery") # Pick up & Delivery
    status = models.CharField(max_length=50, default="Pending") # Pending, Canceled, Preparing, Ready for pick up, On the way, Delivered, & Failed to deliver

class Cart(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField()
    total_amount = models.FloatField(null=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)