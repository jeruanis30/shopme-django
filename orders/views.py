from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem, Cart
from carts.views import _cart_id
from .forms import OrderForm, OrderStatusForm
import datetime
from .models import Order, OrderProduct, Payment
import json
from store.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from currencies.models import Currency
import decimal
from decimal import Decimal

# Create your views here.

#place_order and payments have the same html template called payments
@login_required(login_url='login')
def payments(request):

    #loading the content of the body
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    #store transaction details inside payment models
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()

    #update the payment database
    order.payment = payment
    #update the is_ordered status
    order.is_ordered = True #order is_ordered setting to true
    order.save()

    #Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        #assign the items to the OrderProducts table
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True #ordereproduct setting ordered to true
        orderproduct.ip = request.META.get('REMOTE_ADDR')
        orderproduct.save()

        #get the id generated after saving orderproduct
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct.variation.set(product_variation)
        #update orderproduct for product_variation
        orderproduct.save()

        #Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #clear cart and CartItms
    cart_items = CartItem.objects.filter(user=request.user)#total user cart_items
    # cart_id_used = []
    # for item in cart_items:
    #     cart_id_used.append(item.cart)

    # cart = Cart.objects.filter(cart_id=cart_id_used[0])
    cart_items.delete()
    # cart.delete()

    #removing unexecuted orders in the database
    is_orders_not_executed = Order.objects.filter(user = request.user, is_ordered=False).exists()
    if is_orders_not_executed:
        orders_not_executed = Order.objects.filter(user = request.user, is_ordered=False)
        for old_orders in orders_not_executed:
            old_orders.delete()
    else:
        pass

    #need to convert here since in email is not covered by the currency converter
    user = request.user
    accounts = Account.objects.get(email=user)
    country = accounts.country
    if country == 'Philippines':
        currency = 'PHP'
    else:
        currency = 'USD'
    current_currency = Currency.objects.get(code=currency)

    if currency != 'PHP':
        factor = current_currency.factor
    else:
        factor=1

    order_total = order.order_total
    amount_total = Decimal(order_total)*factor #must be both decimal
    amount_total = '{:.2f}'.format(Decimal(amount_total))

    #Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user':request.user,
        'order':order,
        'currency':currency,
        'amount_total':amount_total

    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    #Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user
    #if the cart count is 0 redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total=0
    tax = 0

    #getting the currency
    user = request.user
    accounts = Account.objects.get(email=user)
    country = accounts.country
    if country == 'Philippines':
        currency = 'PHP'
    else:
        currency = 'USD'

    #summary of computation
    for cart_item in cart_items:
        total+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax = (12 * total)/100
    #get the location and provide the shipping for that location
    shipping_cost_max = (30 * total)/100

    #shipping set to minimu
    if currency == 'PHP':
        shipping_cost_min = 150
        shipping_cost = max(shipping_cost_max, shipping_cost_min)
    else:
        shipping_cost_min = 8000
        shipping_cost = max(shipping_cost_max, shipping_cost_min)#get the max value for shipping

    #no need to convert here since it willl be converted at its templace
    grand_total = total + tax + shipping_cost
    grand_total ='{:.2f}'.format(Decimal(grand_total))


    if request.method == 'POST':
        form = OrderForm(request.POST)
        zip = request.POST['zip']
        address_line_1 = request.POST['address_line_1']
        if not zip:
            messages.warning(request, 'ZIP is missing!. Suggestion: Update later your ZIP code via edit profile.')
            return redirect('checkout')
        if not address_line_1:
            messages.warning(request, 'Address Line 1 is missing!. Suggestion: Complete later your Address via edit profile. To prevent this warning in the future. Thank you.')
            return redirect('checkout')

        if form.is_valid():
            #store all the billing information indside Order table
            data = Order() #initiate Order class
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zip = form.cleaned_data['zip']
            data.currency = form.cleaned_data['currency']
            data.item_count = form.cleaned_data['item_count']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.shipping = shipping_cost
            data.tax = tax #static
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #Generate order number
            y = int(datetime.date.today().strftime('%Y'))
            d = int(datetime.date.today().strftime('%d'))
            m = int(datetime.date.today().strftime('%m'))
            dt = datetime.date(y,m,d)
            current_date = dt.strftime("%Y%m%d") #20210305
            #then cocatenate the primary key to current_date

            #data.id is generated upon saving
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context={
                'order':order, 'cart_items': cart_items, 'tax':tax, 'total':total, 'grand_total':grand_total, 'shipping_cost':shipping_cost,
                }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')

    else:
        return redirect('checkout')

@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    #get other details from the two items above
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        if payment.status == 'COMPLETED':
            pay_status = 'PAID'
        else:
            pay_status = payment.status

        subtotal = 0
        #looping through the product items
        for i in ordered_products:
            subtotal+=i.product_price*i.quantity

        context = {
            'order': order_number,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'transID': payment.payment_id,
            'orderDate': order.created_at,
            'status': order.status,
            'payment': payment,
            'order': order,
            'pay_status':pay_status,
            'sub_total':subtotal,


        }
        return render(request, 'orders/order_complete.html', context)

    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


@login_required(login_url='login')
def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number)
    payment_id = order.payment
    ordered_products = OrderProduct.objects.filter(payment=payment_id)

    payment = Payment.objects.get(payment_id=payment_id)
    if payment.status == 'COMPLETED':
        pay_status = 'PAID'
    else:
        pay_status = payment.status

    subtotal = 0
    #looping through the product items
    for i in ordered_products:
        subtotal+=i.product_price*i.quantity

    context = {
        'order': order_number,
        'ordered_products': ordered_products,
        'order_number': order_number,
        'transID': payment.payment_id,
        'orderDate': order.created_at,
        'status': order.status,
        'payment': payment,
        'order': order,
        'pay_status':pay_status,
        'sub_total':subtotal,
    }

    return render(request, 'orders/order_detail.html', context)

@login_required(login_url='login')
def update_order_status(request, pk):
    user = request.GET.get('usr')
    transID = request.GET.get('trans')
    order = Order.objects.get(payment__payment_id=pk, is_ordered=True)
    form = OrderStatusForm(instance=order)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

        #update the status of orderproducts
        orderproduct = OrderProduct.objects.filter(ordered=True, payment__payment_id=pk)
        for item in orderproduct:
            orderproduct_single = OrderProduct.objects.get(ordered=True, payment__payment_id=pk, product__product_name=item)
            form = OrderStatusForm(request.POST, instance=orderproduct_single)
            if form.is_valid():
                form.save()

        messages.success(request, 'Successfully updated the Order Status.')
        return redirect('dashboard')
    context = {'form': form, 'transID':transID}
    return render(request, 'orders/update_order_status.html', context)


@login_required(login_url='login')
def deleted_order(request, pk):
    order = Order.objects.get(payment__payment_id=pk, user=request.user)
    if request.method == 'POST':
        deleted = request.POST['deleted']
        if deleted == 'deleted':
            order.status = 'Deleted'
            order.save()
            return redirect('dashboard')


#for admin only
@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(payment__payment_id=pk)
    if request.method == 'POST':
        order.delete()
        messages.warning(request, 'Successfully deleted the item.')
        return redirect('dashboard')


@login_required(login_url='login')
def item_recieved(request, order_number):
    order = Order.objects.get(user=request.user, order_number=order_number)
    if request.method == 'POST':
        recieved = request.POST['recieved']
        if recieved == '1':
            order.recieved = True
            order.save()
            messages.success(request, 'Thank you for confirming recieved.')
            return redirect('dashboard')
