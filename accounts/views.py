from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, EditProfileForm, UserProfilePicForm, PwdChangeForm, LoginForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from orders.models import OrderProduct, Order

#verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.models import CartItem, Cart
from carts.views import _cart_id
from store.models import Product
from django.db.models import Q
import requests

from django.core.exceptions import ValidationError
from django.http import HttpResponse

# Create your views here.

def register(request):
    if request.method == 'POST':
        #form will hold all the data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['confirm_password']
            username = email.split('@')[0]

            user = Account.objects.all()
            username_list =[]
            for n in user:
                username_list.append(n.username)
            for uname in username_list:
                if username == uname:
                    username = username + str(-3)
                    num = username.split('-')[1]
                    ustring = username.split('-')[0]
                    conv_num = int(num)
                    num = conv_num+1
                    username = ustring+'-'+str(num)

                else:
                    username == username

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone=phone
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #useractivation end

            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it')
            return redirect('/accounts/login?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context= {'form':form}
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=auth.authenticate(email=email, password=password)
        orderproduct = OrderProduct.objects.filter(user=user)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) #get the session id
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    products=[]
                    #identify the products name
                    for i in cart_item:
                        product_id = i.product_id
                        product = Product.objects.get(id=product_id)
                        products.append(product)

                    #collect the product's name from the cart (products=[]) = (cart_item_cart_list=[])
                    cart_item_cart_list=[]
                    for p in products:
                        cart_item_cart = CartItem.objects.filter(product=p, cart=cart) #all the items in this cart id is in the cart item
                        cart_item_cart_list.append(cart_item_cart)

                    item_carts={}
                    for item in cart_item_cart_list:
                        for i in item:
                            id=i.id
                            qty = i.quantity
                            prod_id = i.product_id
                            variation = i.variations.all()
                            variation = list(variation)
                            variation=str(variation)
                            item_carts[variation+str(prod_id)]=(str(qty) + '-' + str(id))

                    #get the existing cartitem from the user to access his product variation
                    cart_item_user = CartItem.objects.filter(user=user)
                    id=[]
                    item_user=[]
                    for item in cart_item_user:
                        id.append(item.id) #ids of products of the user

                    for item in cart_item_user:
                        qty = item.quantity
                        prod_id = item.product_id
                        variation = item.variations.all()
                        variation = list(variation) #remove the queryset
                        variation=str(variation)
                        item_user.append(variation+str(prod_id))

                    id_cart =[]
                    for key, value in item_carts.items():
                        if key in item_user:
                            index = item_user.index(key)
                            item_id = id[index] #taking the id of existing
                            item = CartItem.objects.get(id=item_id)
                            qty_value=int(value.split('-')[0])
                            id_used = int(value.split('-')[1])
                            id_cart.append(id_used)
                            item.quantity +=qty_value
                            item.user = user
                            item.save()

                        else:
                            if len(id_cart) == 0:
                                for item in cart_item:
                                    item.user = user
                                    item.save()

                            else:
                            #remove the initial products that has been added already in the existing
                                for i in id_cart:
                                    del_cart_item = CartItem.objects.get(id=id_cart[id_cart.index(i)])
                                    cart_item = CartItem.objects.filter(cart=cart).exclude(id=id_cart[id_cart.index(i)])
                                    for item in cart_item:
                                        item.user = user
                                        item.save()

                                    del_cart_item.delete()
                    url = request.META.get('HTTP_REFERER')
                    cart_item_user = CartItem.objects.filter(user=user) #need to redeclare as its value changed
                    if cart_item_user.count() > 0: #with cartitem
                        try:
                            query = requests.utils.urlparse(url).query
                            #next=/cart/checkout/
                            params = dict(x.split('=') for x in query.split('&'))
                            #{next:'/cart/checkout/'}
                            if 'next' in params:
                                nextPage = params['next']
                                auth.login(request, user)
                                messages.success(request, 'You are now loggedin.')
                                return redirect(nextPage)
                        except:
                            pass
                    elif orderproduct.count() > 0:  #with orderproduct
                        auth.login(request, user)
                        messages.success(request, 'You are now loggedin.')
                        return redirect('dashboard')

                    else:
                        auth.login(request, user)
                        auth.login(request, user)
                        return redirect('home')
                else:
                    auth.login(request, user)
                    cart_item_user = CartItem.objects.filter(user=user)
                    if cart_item_user.count() > 0: #with cartitem
                        auth.login(request, user)
                        return redirect('checkout')
                    elif orderproduct.count() > 0: #with orderproduct
                        auth.login(request, user)
                        return redirect('dashboard')
                    else:
                        auth.login(request, user)
                        return redirect('home')

            except Cart.DoesNotExist: #did not order while logged out just loggedin
                auth.login(request, user)
                cart_item_user = CartItem.objects.filter(user=user)
                if cart_item_user.count() > 0: #with cartitem
                    auth.login(request, user)
                    return redirect('checkout')
                elif orderproduct.count() > 0: #with orderproduct
                    auth.login(request, user)
                    return redirect('dashboard')
                else:
                    auth.login(request, user)
                    return redirect('home')
        else: #user is None
            messages.warning(request, 'Username or Password is incorrect!')
            return redirect('login')
    else: #request not a POST
        form=LoginForm()
        context={'form':form}
        return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'logout successful')
    return redirect('login')

def activate(request, uidb64, token):
    #decode the ids
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is now active. Please Login below.')
        messages.warning(request, 'Your email [ ' + str(user) + ' ]')
        return redirect('login')
    else:
        messages.warning(request, 'Invalid activation link')
        return redirect('register')

def forgotPasswordResetValidate(request, uidb64, token):
        #decode the ids
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user=None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Please reset your password')
            return redirect('forgotPasswordReset_page')
        else:
            messages.warning(request, 'This link has been expired')
            return redirect('login')

def forgotPasswordReset_page(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful, login below.')
            return redirect('login')
        else:
            messages.warning(request, 'Password do not match.')
            return redirect('forgotPasswordReset_page')
    else:
        return render(request, 'accounts/forgotPasswordReset_page.html')

@login_required(login_url = 'login')
def dashboard(request):
    current_user = request.user
    if current_user.is_admin or current_user.is_superadmin:
        order = Order.objects.all().filter(is_ordered=True)
        count = order.count()
        delivered = Order.objects.filter(status='Delivered')
        delivered_count=delivered.count()
        OFD = Order.objects.filter(status='Out for delivery')
        OFD_count = OFD.count()
        pending = Order.objects.filter(status='Pending')
        pending_count = pending.count()
        cancel = Order.objects.filter(status='Cancelled')
        cancel_count = cancel.count()


    else:
        order = Order.objects.filter(~Q(status='Deleted'), user=current_user, is_ordered=True).order_by('-id')
        count = order.count()
        delivered = Order.objects.filter(user=current_user, status='Delivered')
        delivered_count=delivered.count()
        OFD = Order.objects.filter(user=current_user, status='Out for delivery')
        OFD_count = OFD.count()
        pending = Order.objects.filter(user=current_user, status='Pending')
        pending_count = pending.count()
        cancel = Order.objects.filter(user=current_user, status='Cancelled')
        cancel_count = cancel.count()


    context = {'order':order, 'count':count,'delivered':delivered_count,'OFD':OFD_count,'pending':pending_count,'cancel':cancel_count}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url = 'login')
def dashboard_single(request):
    current_user = request.user
    if current_user.is_admin or current_user.is_superadmin:
        orderproducts = OrderProduct.objects.all().filter(ordered=True).order_by('-updated_at')

        #get productsorder count
        count = orderproducts.count()
        delivered = OrderProduct.objects.filter(status='Delivered')
        delivered_count=delivered.count()
        OFD = OrderProduct.objects.filter(status='Out for delivery')
        OFD_count = OFD.count()
        pending = OrderProduct.objects.filter(status='Pending')
        pending_count = pending.count()
        cancel = OrderProduct.objects.filter(status='Cancelled')
        cancel_count = cancel.count()

    else:
        orderproducts = OrderProduct.objects.filter(user=current_user, ordered=True).order_by('-updated_at')
        count = orderproducts.count()
        delivered = OrderProduct.objects.filter(user=current_user, status='Delivered')
        delivered_count=delivered.count()
        OFD = OrderProduct.objects.filter(user=current_user, status='Out for delivery')
        OFD_count = OFD.count()
        pending = OrderProduct.objects.filter(user=current_user, status='Pending')
        pending_count = pending.count()
        cancel = OrderProduct.objects.filter(user=current_user, status='Cancelled')
        cancel_count = cancel.count()

    context = {'orderproducts':orderproducts, 'count':count,'delivered':delivered_count,'OFD':OFD_count,'pending':pending_count,'cancel':cancel_count}
    return render(request, 'accounts/dashboard_single.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #RESET PASSWRD EMAIL
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('accounts/forgotPassword_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #useractivation end
            # messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('/accounts/login?command=pwdvalidation&email='+email)
        else:
            messages.warning(request, 'Account does not exists.')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')

@login_required(login_url = 'login')
def my_profile(request):
    info = Account.objects.get(email=request.user)
    context = {'info': info}
    return render(request, 'accounts/my_profile.html', context)

@login_required(login_url = 'login')
def edit_profile(request):
    accounts = Account.objects.get(email=request.user)
    user_country = accounts.country
    if request.method == 'POST':
        propic_form = UserProfilePicForm(request.POST, request.FILES, instance=accounts)
        form = EditProfileForm(request.POST, instance=accounts)
        if form.is_valid() and propic_form.is_valid():
            propic_form.save()
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone']
            user.profession = form.cleaned_data['profession']
            user.address_line_1 = form.cleaned_data['address_line_1']
            user.address_line_2 = form.cleaned_data['address_line_2']
            user.country = form.cleaned_data['country']
            user.state = form.cleaned_data['state']
            user.city = form.cleaned_data['city']
            user.zip = form.cleaned_data['zip']
            user.save()
            messages.success(request, 'Your profile has been successfully updated.')
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=accounts)
        propic_form = UserProfilePicForm(instance=accounts)

    context={'form':form, 'accounts':accounts, 'propic_form':propic_form, 'user_country':user_country}
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url = 'login')
def change_password(request):
     accounts = Account.objects.get(email=request.user)
     if request.method == 'POST':
         current_password = request.POST['old_password']
         new_password = request.POST['new_password2']
         form = PwdChangeForm(request.POST, instance=accounts)
         if form.is_valid():
            success = accounts.check_password(current_password)
            if success:
                 accounts.set_password(new_password)
                 accounts.save()
                 messages.success(request, 'Login with your new password.')
                 return redirect('login')
            else:
                messages.warning(request, 'Password update Fail! You provided a wrong Old Password.')
                return redirect('change_password')
     else:
         form = PwdChangeForm(instance=accounts)
     context = {'accounts':accounts, 'form':form}
     return render(request, 'accounts/change_password.html', context)
