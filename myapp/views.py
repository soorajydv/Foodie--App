from audioop import reverse

from django.views import View
from .models import Order
from django.shortcuts import get_object_or_404, render, redirect
import json
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
from .models import FeatureProduct, FoodItem, Cart, contact
from django.contrib.auth.models import User
from .forms import CheckoutForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page
            messages.success(request, 'Login Successful')

            return redirect('home')

        else:
            messages.error(request, 'username & password may be invalid')
            return redirect('login_view')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Attempt to create a new user
        if User.objects.filter(username=username).exists():
            error_message = 'Username is already taken. Please choose a different username.'
            return render(request, 'signup.html', {'error_message': error_message})

        else:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
            messages.success(
                request, "your account has been created successfully")

            # Redirect or perform additional actions for successful signup
            return redirect('login_view')

    # Display an error message when the username is already taken
    else:
        return render(request, 'signup.html')


def home(request):
    feature_items = FeatureProduct.objects.all()
    food_items = []

    for item in feature_items:
        food_items.append(item.food_items)

    context = {
        'food_items': food_items,
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)

    return render(request, 'home.html', context)


def contact_view(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject = request.POST['message']

        contact.objects.create(name=name, phone=phone, email=email, subject=subject)
       
        return redirect("home")
    
     #########
    context = {}

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    #######

    
    return render(request, 'contact.html',context)


# def menu(request):
#     return render(request, 'menu.html')


def menu(request):
    food_items = FoodItem.objects.all()
    print('foooooood:  ',food_items)

    #########
    context = {
        'food_items': food_items,
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    #######
    return render(request,'menu.html',context)


def cart(request):
    user = User.objects.get(id=request.user.id)
    # product=FoodItem.objects.filter(id=product_id)
    cart_items = Cart.objects.filter(user=user, isClear=False)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.product.quantity


    #################
    context = {
        "cart_items": cart_items
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    ####################
    return render(request, 'cart.html', context)


all_cart_items = []
def go_to_cart(request):
    global all_cart_items
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)
        print(data)

        # Process the JSON data
        cart_items = FoodItem.objects.filter(id__in=data['products'])
        all_cart_items = cart_items

        print(cart_items)
        # Return the JSON response
        return render(request, 'cart.html',)
    else:
        cart_items = all_cart_items
        all_cart_items = []
    # return render(request, 'cart.html', {'cart_items':[{'name':'One'},{'name':'Two'}]} )
    return render(request, 'cart.html', {'cart_items': cart_items})




    # store order information(checkout form)

import uuid

def checkout_view(request):
    #fetching total amount
    user = User.objects.get(id=request.user.id)
    cart_items = Cart.objects.filter(user=user,isClear=False)
    products = [item.product.price for item in cart_items]
    total_amount = sum(products)
    url = "https://uat.esewa.com.np/epay/transrec"

    data = {
        'amt':total_amount,
        'scd':'EPAYTEST',
        'rid':"refid"+str(user.id),  # user.id is initial use oredr id for specific order
    
        'pid': uuid.uuid4()
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            
            return render(request, 'esewa.html', {'total_amount':total_amount})
            # Process the form data here (e.g., save to the database)
            # Redirect or perform other actions after successful submission
    
    form = CheckoutForm()

    #########
    context = {'form': form, 'dynamic_total_amount':total_amount}

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    #######
    return render(request, 'checkout.html', context )


def checkout(request):
    if request.method == 'POST':
        print('Post req')
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Retrieve the total amount from the hidden input field
            total_amount = request.POST.get('order_total', 0)
            order.total = total_amount

            # You can set other fields here, e.g., user, cart, etc.
            order.user = request.user  # If you have user authentication

            order.save()
            print('Order Saved')
            uid = uuid.uuid4()
            print(uid)

            # Redirect to a confirmation page or another URL
            return render(request, 'esewarequest.html', {'uid':uid})
        else:
            print('Form is Invalid')

    print('get req')
    form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})


# Views for cart
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        # Add item to cart
        if product_id > 0:
            user = User.objects.get(id=user_id)
            product = FoodItem.objects.get(id=product_id)
            try:
                cart_item = Cart.objects.get(
                    user=user, isClear=False, product=product)
                print('Added product id', cart_item)
                print(cart_item)
            except Cart.DoesNotExist:
                cart_item = Cart.objects.create(
                    user=user, product=product, qunatity=1)
                print('Product added, : ', cart_item)
            return redirect('home')

        ###
    # return redirect('menu')
    # food_items = FoodItem.objects.all()
    # print('foooooood:  ',food_items)
    # return render(request,'menu.html',{'food_items':food_items})

# def order(request):
#     if request.method == 'POST':


# @csrf_exempt
def verify_payment(self,request):
        url ="https://uat.esewa.com.np/epay/transrec"
        q = request.GET.get('q')
        print(request.GET)
        d = {
            'amt':request.GET.get('amt'),
            'scd': 'EPAYTEST',
            'rid':  request.GET.get('refId'),
            'pid':request.GET.get('oid'),
        }
        resp = request.post(url, d)
        print("status code=====",resp.status_code)
        if resp.status_code == 200:
        # print(resp.text)
            return HttpResponse("Payment Successful")
        else:
            raise Http404()

def paymentsuccess(request):
     #########
    context = {}

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    #######
    return render (request,'paymentsuccess.html', context)

# views.py
# cart/views.py

from django.shortcuts import redirect
from .models import Cart

def delete_cart_item(request,id):
    items = Cart.objects.get(id=id)
    print(items)
    items.delete()
    return render(request,'cart.html',{'items':items})  # Replace 'cart' with the appropriate URL name

