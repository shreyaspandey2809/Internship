from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EventForm
from .models import Event, Registration

User = get_user_model()

# -------------------
# Login View
# -------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.is_staff:
                return redirect('accounts:admin_dashboard')
            return redirect('accounts:student_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")   # 🔑 return render instead of redirect

    return render(request, "login.html")

# -------------------
# Register View
# -------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        role = request.POST.get("role")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        user = User.objects.create_user(username=username, password=password)

        # Role check
        if role == "staff":
            user.is_staff = True
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("accounts:login")

    return render(request, "register.html")

# -------------------
# Forgot Password
# -------------------
def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully. Please login.")
            return redirect("accounts:login")
        except User.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, "forgot_password.html")

# -------------------
# Logout
# -------------------
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

# -------------------
# Student Dashboard
# -------------------
@login_required(login_url="accounts:login")
def student_dashboard(request):
    events = Event.objects.all()
    registrations = Registration.objects.filter(student=request.user)
    return render(request, "student_dashboard.html", {
        "events": events,
        "registrations": registrations
    })

# -------------------
# Register Event
# -------------------
@login_required(login_url="accounts:login")
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.get_or_create(event=event, student=request.user)
    messages.success(request, f"Successfully registered for {event.title}")
    return redirect("accounts:student_dashboard")

# -------------------
# Admin Dashboard
# -------------------
@login_required(login_url="accounts:login")
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized access.")
        return redirect("accounts:student_dashboard")

    events = Event.objects.filter(created_by=request.user)
    participants = Registration.objects.filter(event__created_by=request.user)
    return render(request, "admin_dashboard.html", {
        "events": events,
        "participants": participants
    })

# -------------------
# Add Event
# -------------------
@login_required(login_url="accounts:login")
def add_event(request):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized action.")
        return redirect("accounts:student_dashboard")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect("accounts:admin_dashboard")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = EventForm()

    return render(request, "create_event.html", {"form": form})
from django.shortcuts import get_object_or_404

@login_required(login_url='accounts:login')
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect("accounts:admin_dashboard")  # ✅ Fix redirect
    else:
        form = EventForm(instance=event)

    return render(request, "edit_event.html", {"form": form, "event": event})
