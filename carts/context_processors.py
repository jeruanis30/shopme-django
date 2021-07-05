from .models import Cart, CartItem
from .views import _cart_id
from accounts.models import Account
import json
import requests

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)#total user cart_items
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_items = CartItem.objects.all().filter(cart_id=cart[:1])#only need one result
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)

def country_cur(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    ip_address = '112.206.158.43'
    # ip_address=ip_data['ip'] this is for production
    req = requests.get('http://ip-api.com/json/' + ip_address)
    location = req.text #getting the content into text
    loc_data = json.loads(location)
    country = loc_data['country']
    country_code = loc_data['countryCode']
    user = request.user
    if user.is_authenticated: #use this currency if loggedin
        accounts = Account.objects.get(email=user)
        country = accounts.country
        if country == 'Philippines':
            currency='PHP'
            symbol = '₱'
            country_code = 'PH'
        else:
            currency = 'USD'
            symbol = '$'
            country_code = 'US'
    else:  # this will be the currency when loggedout
        if country == 'Philippines':
            currency='PHP'
            symbol = '₱'
            country_code = 'PH'
        else:
            currency = 'USD'
            symbol = '$'
            country_code = 'US'
    return dict(currency=currency, symbol=symbol)
