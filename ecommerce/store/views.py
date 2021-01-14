from django.shortcuts import render, HttpResponse
from pathlib import Path
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json 
import datetime 

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

        # I like this approach since initially (at least based on how the app is currently structured) there will be no Order object for each customer. 
        # Therefore, what the below get_or_create function will let us do is that when the user first tries to go to the /cart route, a new Order object 
        # will be created. 
        # Upon subsequent visits, the user will basically be "getting" this Order object (as it has already been created already) and therefore, this 
        # function call works. 
        # One caveat though.....if we have created this object, then we need to save it as well. 
        # Therefore, if the variable "created" below returns a True, then we need to save the Order object that has just been created by adding the following 
        # line of code:

        # if created = True:
        #     order.save()

        # The alternative method here would be to simply "get" the correct order based on the value passed in as parameters to the get_or_create function below.
        # So how do we deal with the creation and the subsequent saving of the Order object?
        # Well, we can basically use signals, similar to how you used them to automatically created objects of the Profile model class in the other Django app you were building last week. 
        # This way, whenever a user account is created and saved (hint: post_save signal), it would send a signal to the Order model class which would result 
        # in the creation and saving of an Order object. 

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
            "order.physical_product": 'True'
        }
        items = []
    
    context = {
        "items": items,
        "order": order,
    }
    return render(request, "store/checkout.html", context)




"""
    The following are api functions. 
"""
# @csrf_exempt
def UpdateCart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)

        customer = request.user.customer 
        product = Product.objects.get(pk = data['productid'])
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        
        orderitem, created = OrderItem.objects.get_or_create(order = order, product = product)

        if data['buttontype'] == 'add':
            orderitem.quantity = orderitem.quantity + 1;  
        elif data['buttontype'] == 'remove':
            orderitem.quantity = orderitem.quantity - 1; 
        
        orderitem.save()

        # As per documentation, no need to save anything after the delete() method has been used. 
        if orderitem.quantity <= 0:
            orderitem.delete()

        return JsonResponse(f'{data}', safe=False)
    else: 
        return JsonResponse('gucci2', safe=False)


def get_cart_total_quantity(request):
    
    if request.user.is_authenticated:

        customer = request.user.customer 

        order, created = Order.objects.get_or_create(customer = customer, completed = False)

        # orderitems = self.orderitem.all()
        # TotalQuantityInCart = sum([item.quantity for item in orderitems])
        # print(TotalQuantityInCart)

        TotalQuantityInCart = order.get_item_total_quantity
        return JsonResponse({"TotalQuantityInCart": TotalQuantityInCart})
    else: 
        return JsonResponse('gucci111', safe=False)

        

def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print("Data", data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_item_total_amount:
            order.complete = True
        order.save()

        if order.physical_product == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order, 
                address = data['shipping']['address']
                city = data['shipping']['city']
                state = data['shipping']['state']
                zipcode = data['shipping']['zipcode']
            )


    
    else: 
        print("user is not authenticated")
    return JsonResponse('Payment completed and order processed', safe=False)

