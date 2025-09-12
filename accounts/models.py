from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("staff", "Staff"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    poster = models.ImageField(upload_to="event_posters/", blank=True, null=True)

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="events",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"
