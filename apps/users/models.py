from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    cellphone = models.CharField(max_length=20, blank=True, null=True)
    absence_message = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    

class UserClient(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='user_clients'
    )

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='client_users'
    )

    profile = models.ForeignKey(
        'permissions.Profile',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.client.name}"