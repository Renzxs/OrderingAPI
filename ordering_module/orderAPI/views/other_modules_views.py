from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from ..models import Customer, Product, Rider
from ..serializers import CustomerSerializer, ProductSerializer, RiderSerializer

# ------------- THIS VIEWS ARE NOT BELONG IN THIS MODULE! -----------------------
# ------------------- FOR TESTING PURPOSES ONLY! ------------------------------

# Product CRUD 
class ProductListCreateAPIView(generics.ListCreateAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

# Riders CRUD
class RiderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer

class RiderListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    lookup_field = "pk"

# Customers CRUD
class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "pk"
    
