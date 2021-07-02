from .models import Cart, CartItem
from .views import _cart_id
from accounts.models import Account

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

    user = request.user
    if user.is_authenticated:
        currency=0
        accounts = Account.objects.get(email = user)
        country = accounts.country
        if country == 'Philippines':
            currency = 'PHP'
        else:
            currency = 'USD'
    else:
        currency=''
        country=''
    return dict(cart_count=cart_count, country=country, currency=currency)
