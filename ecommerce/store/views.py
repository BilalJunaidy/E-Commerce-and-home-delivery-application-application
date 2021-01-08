from django.shortcuts import render
from pathlib import Path
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Create your views here.

def store(request):

    products = Product.objects.all()
    context = {
        "products": products 
    }
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer 

        
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem.all()
        
    else: 
        order = {
            "order.get_item_total_quantity":0,
            "order.get_item_total_amount":0,
        }
        items = []
    
    context = {
        "items": items,
        "order": order,
    }

    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem.all()
        
    else: 
        order = {
            "order.get_item_total_quantity":0,
            "order.get_item_total_amount":0,
        }
        items = []
    
    context = {
        "items": items,
        "order": order,
    }
    return render(request, "store/checkout.html", context)