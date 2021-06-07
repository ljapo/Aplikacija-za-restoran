from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *

# Create your views here.
def store(request):

    if request.user.is_authenticated: #Ako je i else ako nije korisnik ulogovan za narudžbe
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #Uzimanje nekog objekta ili kreiranje istog
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    else: 
        items = []
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping':False} #Za guesta, naruddžba je prazna
        cartItems=order['get_cart_items']
       
    products = Product.objects.all()
    context={'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated: #Ako je i else ako nije korisnik ulogovan za narudžbe
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #Uzimanje nekog objekta ili kreiranje istog
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
        
    else: 
        items = []
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping':False} #Za guesta, naruddžba je prazna
        cartItems=order['get_cart_items']
       
    context={'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated: #Ako je i else ako nije korisnik ulogovan za narudžbe
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #Uzimanje nekog objekta ili kreiranje istog
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    else: 
        items = []
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping':False} #Za guesta, naruddžba je prazna
        cartItems=order['get_cart_items']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId=data['productId']
    action=data['action']           #query operacija podataka koje kupimo u Jsonu i Js fileu

    print('Action:', action)
    print('productId:', productId)

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False) #Uzimanje nekog objekta ili kreiranje istog

    orderItem, created=OrderItem.objects.get_or_create(order=order, product=product) #ukoliko postoji već narudžba ne želimo kreirati novi proizvod nego povećati količinu narudžbe

    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1) #stimanje itema u admin panelu

    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def processOrder (request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id

        if total==float(order.get_cart_total):
            order.complete=True
        order.save()

        
        ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'], #Slanje adrese na admin panel
                city=data['shipping']['city'],



)
    else:
        print('Korisnik nije prijavljen.')
    return JsonResponse('Placanje uspjesno!', safe=False)