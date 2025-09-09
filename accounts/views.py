from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

ALLOWED_USERS = []  

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.username in ALLOWED_USERS:
            login(request, user)
            return redirect("/user/")
        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials or not allowed"})

    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # create new user
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)  # auto login after registration
        return redirect('/')  # redirect to homepage or dashboard

    return render(request, 'register.html')

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