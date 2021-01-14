import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except: 
        cart = {}
    print('Cart:', cart)
    items = []
    order = {
        "get_item_total_quantity":0,
        "get_item_total_amount":0,
        'physical_product': False,
    }
    cartItems = order['get_item_total_quantity']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(pk = i)
            total = (product.price * cart[i]['quantity'])
            
            order['get_item_total_amount'] += total
            order['get_item_total_quantity'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': {
                        'url': product.image.url,
                    },
                },
                'quantity': cart[i]['quantity'],
                'get_item_total': total,
            }
            
            items.append(item)
            if product.digital == False:
                order['physical_product'] = True
        except:
            pass
    return {
        'cartItems': cartItems,
        'order': order,
        'items': items, 
        }


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(
    customer=customer,
    complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order