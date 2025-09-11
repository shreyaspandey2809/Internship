from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Auth
    path("", views.login_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("logout/", views.logout_view, name="logout"),

    # Student
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/register-event/<int:event_id>/", views.register_event, name="register_event"),

    # Teacher
    path("teacher/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("teacher/add-event/", views.add_event, name="add_event"),
    path('teacher/edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('teacher/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
]
