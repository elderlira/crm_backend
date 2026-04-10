from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True
    )

    cellphone = models.CharField(max_length=20, blank=True, null=True)
    absence_message = models.TextField(blank=True, null=True)

    role = models.CharField(
        max_length=20,
        choices=[
            ("admin", "Admin"),
            ("supervisor", "Supervisor"),
            ("agent", "Agent"),
        ],
        default="agent"
    )

    is_online = models.BooleanField(default=False)
    last_logout = models.DateTimeField(null=True, blank=True)

    no_auto_assign = models.BooleanField(default=False)
    see_department_tickets = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
class UserDepartment(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="departments"
    )
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="users"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "department")

    def __str__(self):
        return f"{self.user.email} - {self.department.name}"
    
@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    user.is_online = True
    user.save(update_fields=['is_online'])

@receiver(user_logged_out)
def on_user_logout(sender, request, user, **kwargs):
    if user:
        user.is_online = False
        user.last_logout = timezone.now()
        user.save(update_fields=['is_online', 'last_logout'])