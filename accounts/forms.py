from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser , Event

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'venue', 'category']