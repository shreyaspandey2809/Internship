from django.urls import path
from .views import login_view, register_view, dashboard, forgot_password
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('user/', dashboard, name='dashboard'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('', login_view, name='home'),
]
