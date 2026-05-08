from django.db import models
from django.conf import settings
from apps.permissions.models import Permission

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    permissions = models.ManyToManyField(
        Permission, 
        blank=True, 
        related_name="profiles"
    )

    def __str__(self):
        return f"Perfil de Acesso: {self.user.username}"