from django.urls import path
from .views import (
    index,
    ProductListView,
    CreateProductView,
    ProductDetailView,
    UpdateProductView,
    DeleteProductView,
    OrdersListView,
    CreateOrderView,
    OrdersDetailView,
    UpdateOrder, DeleteOrderView
)

app_name = 'shop'
urlpatterns = [
    path('', index, name='index'),
    path('products/', ProductListView.as_view(), name='products'),
    path('createProduct/', CreateProductView.as_view(), name='createProduct'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='productDetails'),
    path('product/<int:pk>/update/', UpdateProductView.as_view(), name='productUpdate'),
    path('product/<int:pk>/archive/', DeleteProductView.as_view(), name='productArchive'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('createOrder/', CreateOrderView.as_view(), name='createOrder'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='ordersDetails'),
    path('orders/<int:pk>/update', UpdateOrder.as_view(), name='updateOrder'),
    path('orders/<int:pk>/archive/', DeleteOrderView.as_view(), name='ordersArchive'),
]
