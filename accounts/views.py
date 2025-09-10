from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, EventForm
from .models import Event, Registration
from django.contrib.auth.decorators import login_required

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('accounts:admin_dashboard')
            else:
                return redirect('accounts:student_dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('accounts:login')

    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        role = request.POST.get("role")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('accounts:register')

        user = User.objects.create_user(username=username, password=password)
        if role == "staff":
            user.is_staff = True
            user.save()

        messages.success(request, "Account created successfully!")
        return redirect('accounts:login')

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
            return redirect("accounts:login")
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")

    return render(request, "forgot_password.html")


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def student_dashboard(request):
    events = Event.objects.all()
    registrations = Registration.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {'events': events, 'registrations': registrations})


@login_required(login_url='accounts:login')
def register_event(request, event_id):
    event = Event.objects.get(id=event_id)
    Registration.objects.get_or_create(event=event, student=request.user)
    return redirect('accounts:student_dashboard')


@login_required(login_url='accounts:login')
def admin_dashboard(request):
    events = Event.objects.filter(created_by=request.user)
    return render(request, 'admin_dashboard.html', {'events': events})


@login_required(login_url='accounts:login')
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('accounts:admin_dashboard')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})
