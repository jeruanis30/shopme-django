from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPasswordResetValidate/<uidb64>/<token>/', views.forgotPasswordResetValidate, name='forgotPasswordResetValidate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('forgotPasswordReset_page/', views.forgotPasswordReset_page, name='forgotPasswordReset_page'),
]
