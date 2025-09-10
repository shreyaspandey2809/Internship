from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    poster = models.ImageField(upload_to="event_posters/", blank=True, null=True)

    # allow null=True + blank=True so old rows won’t break
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="events",
        null=True,     # ✅ fixes migration issue
        blank=True     # ✅ allows empty in admin/forms if needed
    )

    def __str__(self):
        return self.title


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"
