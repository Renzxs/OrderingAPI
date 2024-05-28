from django.urls import path
from .views.order_views import GetOrders, CreateOrder, UpdateOrder, DeleteOrder
from .views.cart_views import GetCart, CreateCart, UpdateCart, DeleteCart
from .views.other_modules_views import CustomerListCreateAPIView, CustomerListUpdateDeleteView, ProductListCreateAPIView, ProductListUpdateDeleteView, RiderListCreateAPIView, RiderListUpdateDeleteView

urlpatterns = [
    # Order API URLs
    path('get-orders/', GetOrders.as_view(), name="get-orders"),
    path('create-order/', CreateOrder.as_view(), name="create-order"),
    path('update-order/<int:pk>/', UpdateOrder.as_view(), name="update-order"),
    path('delete-order/<int:pk>/', DeleteOrder.as_view(), name="delete-order"),

    # Cart API URLs
    path('get-cart/', GetCart.as_view(), name="get-cart"),
    path('create-cart/', CreateCart.as_view(), name="create-cart"),
    path('update-cart/<int:pk>/', UpdateCart.as_view(), name="update-cart"),
    path('delete-cart/<int:pk>/', DeleteCart.as_view(), name="delete-cart"),

    # ----------- Other APIs Urls (Not belong in this module!) --------------------
    path('customers/', CustomerListCreateAPIView.as_view(), name="customers-list-create"),
    path('customers/<int:pk>/', CustomerListUpdateDeleteView.as_view(), name="customers-list-update-destroy"),

    path('products/', ProductListCreateAPIView.as_view(), name="products-list-create"),
    path('products/<int:pk>/', ProductListUpdateDeleteView.as_view(), name="products-list-update-destroy"),

    path('riders/', RiderListCreateAPIView.as_view(), name="riders-list-create"),
    path('riders/<int:pk>/', RiderListUpdateDeleteView.as_view(), name="riders-list-update-destroy"),
]