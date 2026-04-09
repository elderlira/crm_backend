from django.contrib.auth.models import AbstractUser
from django.db import models


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