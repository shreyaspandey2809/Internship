from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Event, Registration
from .forms import EventForm
from django.contrib.auth import get_user_model

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == "staff" :
                return redirect("accounts:admin_dashboard")
            elif user.role == "student":
                return redirect("accounts:student_dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role = role
            )

            if role == "staff":
                user.is_staff = True
            elif role == "student":
                user.is_staff = False

            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("accounts:login")

    return render(request, "accounts/register.html")



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

    return render(request, "accounts/forgot_password.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required(login_url="accounts:login")
def student_dashboard(request):
    events = Event.objects.all()
    registrations = Registration.objects.filter(student=request.user)
    return render(request, "accounts/student_dashboard.html", {
        "events": events,
        "registrations": registrations
    })


@login_required(login_url="accounts:login")
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.get_or_create(event=event, student=request.user)

    if event.created_by.email:
        send_mail(
            subject=f"New Registration for {event.title}",
            message=f"{request.user.username} has registered for your event '{event.title}'.",
            from_email=None,
            recipient_list=[event.created_by.email],
            fail_silently=False,
        )

    return redirect("accounts:student_dashboard")


@login_required(login_url="accounts:login")
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized access.")
        return redirect("accounts:student_dashboard")

    events = Event.objects.filter(created_by=request.user)
    participants = Registration.objects.filter(event__created_by=request.user)
    return render(request, "accounts/admin_dashboard.html", {
        "events": events,
        "participants": participants
    })


@login_required(login_url="accounts:login")
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()

            students = User.objects.filter(is_staff=False)
            recipient_list = [s.email for s in students if s.email]
            send_mail(
                subject=f"New Event: {event.title}",
                message=f"A new event '{event.title}' is scheduled on {event.date}. Login to register!",
                from_email=None,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            messages.success(request, "Event created and notifications sent!")
            return redirect("accounts:admin_dashboard")
    else:
        form = EventForm()
    return render(request, "accounts/add_event.html", {"form": form})


@login_required(login_url='accounts:login')
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect("accounts:admin_dashboard")
    else:
        form = EventForm(instance=event)

    return render(request, "accounts/edit_event.html", {"form": form, "event": event})

@login_required(login_url='accounts:login')
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('accounts:admin_dashboard')
    return render(request, "accounts/confirm_delete.html", {"event": event})