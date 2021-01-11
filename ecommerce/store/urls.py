from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart/', views.UpdateCart, name = 'update_cart'),
    path('get_cart_total_quantity/', views.get_cart_total_quantity, name = "get_cart_total_quantity"),
]

