import django_filters
from django_filters import DateFilter, CharFilter
from .models import Product
from django import forms


class ProductPriceFilter(django_filters.FilterSet):
    min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
 # CharFilter(field_name=None, lookup_expr=None, *, label=None, method=None, distinct=False, exclude=False, **kwargs)

    class Meta:
        model = Product  #filtering the Order
        fields = ['price']
