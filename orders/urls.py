from django.urls import path
from . import views

urlpatterns = [
    # path('payments/', views.place_order, name='place_order'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('update_order_status/<int:pk>', views.update_order_status, name='update_order_status'),
    path('order_detail/<str:trans_id>/', views.order_detail, name='order_detail'),
]
