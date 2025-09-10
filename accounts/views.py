from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # ✅ Always send to dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect("dashboard")

    return render(request, "register.html")


def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully. You can now log in.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")

    return render(request, "forgot_password.html")

def dashboard(request):
    return render(request, "dashboard.html")
