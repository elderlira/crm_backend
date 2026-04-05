from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ADMIN = 1
    GERENTE = 2
    USER = 3
    
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (GERENTE, 'Gerente'),
        (USER, 'User'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Company(models.Model):

    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="departments"
    )
    # Adicione esta linha para o switch do Vue funcionar:
    is_active = models.BooleanField(default=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Role(models.Model):
    # Definimos constantes para facilitar o uso no código
    ADMIN = 1
    GERENTE = 2
    USER = 3
    
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (GERENTE, 'Gerente'),
        (USER, 'User'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    phone = models.CharField(max_length=11,blank=True,null=True)
    is_online=models.BooleanField(default=False)
    last_login_at=models.DateTimeField(blank=True, null=True)
    last_logout_at=models.DateTimeField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)

    # Helper para verificar permissões no código
    @property
    def is_admin(self):
        return self.role_id == Role.ADMIN

    @property
    def is_gerente(self):
        return self.role_id == Role.GERENTE