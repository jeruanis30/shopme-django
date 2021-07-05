from django.contrib import admin
from .models import Payment, Order, OrderProduct

class OrderPrductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra  = 0 #remove excess rows

class OrderProductAdmin(admin.ModelAdmin):
    list_display  = ('payment', 'user', 'product', 'quantity', 'created_at', 'ordered', 'status')
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    list_filter = ('ordered',)
    search_fields = ('product__product_name','user__email', 'payment__payment_id')
    fields=['payment', 'variation', 'status', 'ip', 'user', 'product', 'quantity', 'product_price', 'ordered', 'recieved']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'currency', 'order_total', 'status', 'payment', 'is_ordered')
    list_filter = ('status', 'is_ordered')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_per_page = 20 #records
    inlines = [OrderPrductInline] #append OrderProduct at the bottom of Order

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount_paid', 'status')

# Register your models here.
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
