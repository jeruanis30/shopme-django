from django.urls import path
from . import views

urlpatterns = [
    # path('payments/', views.place_order, name='place_order'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('item_recieved/<int:order_number>/', views.item_recieved, name='item_recieved'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('update_order_status/<str:pk>/', views.update_order_status, name='update_order_status'),
    path('deleted_order/<str:pk>/', views.deleted_order, name='deleted_order'),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name='deleteOrder'),
    path('order_detail/<int:order_number>/', views.order_detail, name='order_detail'),
]
