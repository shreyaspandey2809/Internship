from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Event, Registration

User = get_user_model()

# Register User model
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser")

# Register Event model
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "created_by")
    search_fields = ("title",)
    list_filter = ("date", "created_by")

# Register Registration model
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "event")
    search_fields = ("student__username", "event__title")
    list_filter = ("event",)
