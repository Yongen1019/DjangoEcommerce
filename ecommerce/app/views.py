from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Order, Payment, Product, Cart, Wishlist
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
# decorator, fn represents the def being decorated
def cart_total(function):
    def inner(request, id='', *args):
        totalitem = 0

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        # args must be iterable item like sting, list, tuple ...
        args = [totalitem]

        if not id == '':
            return function(request, id, *args)
        return function(request, *args)

    return inner

@login_required
@cart_total
def home(request, *variable):
    context = {
        'totalitem': variable[0]
    }
    return render(request, 'app/home.html', context)

@login_required
@cart_total
def about(request, *variable):
    context = {
        'totalitem': variable[0]
    }
    return render(request, 'app/about.html', context)

@login_required
@cart_total
def contact(request, *variable):
    context = {
        'totalitem': variable[0]
    }
    return render(request, 'app/contact.html', context)

@method_decorator(login_required, name='dispatch')
@method_decorator(cart_total, name='dispatch')
class CategoryView(View):
    def get(self, request, id, *variable):
        
        product = Product.objects.filter(category=id)
        title = Product.objects.filter(category=id)
        # total = Count to count the quantity of {title}
        # title = Product.objects.filter(category=id).values('title').annotate(total=Count('title'))
        
        context = {
            'product': product,
            'title': title,
            'totalitem': variable[0]
            }
        # locals is a built-in function to pass all the local variables to the html template, but it is a bad practice since some variables are not neccessary to be passed
        # return render(request, "app/category.html", locals())
        return render(request, 'app/category.html', context)
    
@method_decorator(login_required, name='dispatch')
@method_decorator(cart_total, name='dispatch')
class CategoryTitle(View):
    def get(self, request, id, *variable):
        
        product = Product.objects.filter(title=id)
        title = Product.objects.filter(category=product[0].category)
        
        context = {
            'product': product,
            'title': title,
            'totalitem': variable[0]
            }
        # locals is a built-in function to pass all the local variables to the html template, but it is a bad practice since some variables are not neccessary to be passed
        # return render(request, "app/category.html", locals())
        return render(request, 'app/category.html', context)
    
@method_decorator(login_required, name='dispatch')
@method_decorator(cart_total, name='dispatch')
class ProductDetail(View):
    def get(self, request, id, *variable):

        # pk = primary key (auto generated)
        product = Product.objects.get(pk=id)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        
        context = {
            'product': product,
            'wishlist': wishlist,
            'totalitem': variable[0]
            }
        return render(request, 'app/productdetail.html', context)
    
class CustomerRegistrationView(View):
    @method_decorator(cart_total, name='dispatch')
    def get(self, request, *variable):
        form = CustomerRegistrationForm()

        context = {
            'form': form,
            'totalitem': variable[0]
            }
        return render(request, 'app/customer-registration.html', context)
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        
        context = {
            'form': form
        }
        return render(request, 'app/customer-registration.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    @method_decorator(cart_total, name='dispatch')
    def get(self, request, *variable):
        form = CustomerProfileForm()

        context = {
            'form': form,
            'totalitem': variable[0]
        }
        return render(request, 'app/profile.html', context)
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            # database map
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        context = {
            'form': form
        }
        return render(request, 'app/profile.html', context)
        
@login_required
@cart_total
def address(request, *variable):
    address = Customer.objects.filter(user=request.user)

    context = {
        'address': address,
        'totalitem': variable[0]
    }
    return render(request, 'app/address.html', context)

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    @method_decorator(cart_total, name='dispatch')
    def get(self, request, id, *variable):
        address = Customer.objects.get(pk=id)
        # all the data will be automatically filled into the form field
        form = CustomerProfileForm(instance=address)
        
        context = {
            'address': address,
            'form': form,
            'totalitem': variable[0]
        }
        return render(request, 'app/update-address.html', context)

    def post(self, request, id):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            address = Customer.objects.get(pk=id)
            address.name = form.cleaned_data['name']
            address.locality = form.cleaned_data['locality']
            address.city = form.cleaned_data['city']
            address.mobile = form.cleaned_data['mobile']
            address.state = form.cleaned_data['state']
            address.zipcode = form.cleaned_data['zipcode']
            address.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return redirect("address")

@login_required
def add_to_cart(request):
    user = request.user
    productID = request.GET['prod_id']
    product = Product.objects.get(id=productID)
    
    # Cart.objects.get(Q(product=productID) & Q(user=request.user)) will raise an error if data not exist, if data exists execute else part, if data not exist execute except part
    try:
        Cart.objects.get(Q(product=product) & Q(user=request.user))
        
    except:
        Cart(user=user, product=product).save()

    else:
        cartProduct = Cart.objects.get(Q(product=product) & Q(user=request.user))
        cartProduct.quantity += 1
        cartProduct.save()
    
    return redirect("cart")

@login_required
@cart_total
def cart(request, *variable):
    user = request.user
    cart = Cart.objects.filter(user=user)
    
    amount = 0
    for item in cart:
        amount += (item.quantity * item.product.discounted_price)
    shipping = 4.00
    totalamount = round(amount + shipping, 2)
    
    context = {
        'cart': cart,
        'amount': amount,
        'shipping': shipping,
        'totalamount': totalamount,
        'totalitem': variable[0]
    }
    return render(request, 'app/cart.html', context)

def modify_cart(request):
    if request.method == 'GET':
        productID = request.GET['productID']
        product = Product.objects.get(id=productID)
        # Q is required for multiple filter conditions
        cartProduct = Cart.objects.get(Q(product=product) & Q(user=request.user))

        action = request.GET['action']
        if action == 'add':
            cartProduct.quantity += 1
        elif action == 'minus':
            cartProduct.quantity -= 1
            
        quantity = cartProduct.quantity
        cartProduct.save()

        if action == 'remove':
            cartProduct.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0
        for item in cart:
            amount += (item.quantity * item.product.discounted_price)
        shipping = 4.00
        totalamount = round(amount + shipping, 2)

        context = {
            'quantity': quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(context)
    
@method_decorator(login_required, name='dispatch')
class checkOut(View):
    @method_decorator(cart_total, name='dispatch')
    def get(self, request, *variable):
        user = request.user
        address = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)

        amount = 0
        for item in cart:
            amount += (item.quantity * item.product.discounted_price)
        shipping = 4.00
        totalamount = round(amount + shipping, 2)

        order_id = '1'
        order_status = 'created'
        # payment = Payment(
        #     user = user,
        #     amount = totalamount,
        #     razerpay_order_id = order_id,
        #     razerpay_payment_status = order_status
        # )
        # payment.save()

        context = {
            'address': address,
            'cart': cart,
            'amount': amount,
            'shipping': shipping,
            'totalamount': totalamount,
            'totalitem': variable[0]
        }
        return render(request, 'app/checkout.html', context)
    
@login_required
def payment_done(request):
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id = cust_id)
    payment = Payment.objects.get(razerpay_order_id = 1)
    payment.paid = True
    payment.razerpay_payment_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user = user)

    for item in cart:
        Order(user=user, customer=customer, product=item.product, quantity=item.quantity, payment=payment).save()
        item.delete()

    return redirect('order')

@login_required
@cart_total
def order(request, *variable):
    order = Order.objects.filter(user=request.user)

    context = {
        'order': order,
        'totalitem': variable[0]
    }
    return render(request, 'app/order.html', context)

@login_required
@cart_total
def wishlist(request, *variable):
    wishlist = Wishlist.objects.filter(user=request.user)

    context = {
        'wishlist': wishlist,
        'totalitem': variable[0]
    }
    return render(request, 'app/wishlist.html', context)

def modify_wishlist(request):
    if request.method == 'GET':
        user = request.user
        productID = request.GET['productID']
        product = Product.objects.get(id=productID)
        
        try:
            wishlistProduct = Wishlist.objects.get(Q(product=product) & Q(user=request.user))
            
        except:
            Wishlist(user=user, product=product).save()
            message = 'Wishlist added'

        else:
            wishlistProduct.delete()
            message = 'Wishlist removed'
    
    context = {
        'message': message
    }
    return JsonResponse(context)

@login_required
@cart_total
def search(request, *variable):
    query = request.GET['search']
    # filter product title which contains search query
    product = Product.objects.filter(Q(title__icontains=query))

    context = {
        'product': product,
        'totalitem': variable[0]
    }
    return render(request, "app/search.html", context)
    