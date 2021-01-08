from django.contrib import admin
from .models import Customer, Product, ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User 


# Register your models here.

# No need to register the User model here since we are using Django's default User model....which is already registered by Django.  
# admin.site.register(User)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

