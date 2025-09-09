from django.urls import path
from . import views
from .views import *
from django.urls import path, include
from django.shortcuts import render


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('user/', dashboard , name = 'dashboard'),
    path('', login_view, name='home'),
    path('forgot-password/', forgot_password, name='forgot_password'),
]