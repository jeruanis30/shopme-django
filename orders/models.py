from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100) #transactionID
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refund_Paid', 'Refund_Paid'),
        ('Deleted', 'Deleted')
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=21)
    first_name = models.CharField(max_length=54)
    last_name = models.CharField(max_length=54)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=51)
    address_line_1 = models.CharField(max_length=51)
    address_line_2 = models.CharField(max_length=51, blank=True)
    country = models.CharField(max_length=54)
    state = models.CharField(max_length=54)
    city = models.CharField(max_length=54)
    zip = models.IntegerField(null=True, blank=True)
    order_note = models.CharField(max_length=200, blank=True)
    currency = models.CharField(max_length=10, blank=True)
    item_count = models.IntegerField(null=True)
    order_total = models.FloatField()
    shipping = models.FloatField(null=True)
    recieved = models.BooleanField(default=False)
    tax = models.FloatField()
    status = models.CharField(max_length=25, choices=STATUS, default='Pending')
    ip = models.CharField(max_length=21, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def address(self):
        return f'{self.address_line_1} {self.address_line_2}, {self.city}, {self.state}, {self.country}, {self.zip}'

    def __unicode__(self):
        return self.user.usernmae


class OrderProduct(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refund_Paid', 'Refund_Paid')
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=25, null=True, choices = STATUS, default='Pending')
    ip = models.CharField(max_length=21, blank=True)
    recieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.product_name

    def date_updated(self):
        return self.updated_at.strftime('%B %d %Y') #converting to Month name, day and Year pattern
