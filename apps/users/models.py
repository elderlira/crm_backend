from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    company = models.ForeignKey(
        'company.Company', 
        on_delete=models.CASCADE, 
        related_name='users'
    )
    
    role = models.ForeignKey(
        'permissions.Profile', 
        on_delete=models.PROTECT, 
        related_name='users',
        null=True,
        blank=True
    )
    
    away_message = models.TextField(blank=True, null=True)
    no_auto_assign = models.BooleanField(default=False)
    see_department_tickets = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Último Login")
    last_logout = models.DateTimeField(null=True, blank=True, verbose_name="Último Logout")
    is_online = models.BooleanField(default=False, verbose_name="Status Online")


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    def __str__(self):
        return self.email

class UserDepartment(models.Model):
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='user_departments'
    )
    department = models.ForeignKey(
        'departments.Department', 
        on_delete=models.CASCADE, 
        related_name='user_links'
    )

    class Meta:
        unique_together = ('user', 'department')
        verbose_name = "Departamento do Usuário"
        verbose_name_plural = "Departamentos dos Usuários"

    def __str__(self):
        return f"{self.user.email} -> {self.department.name}"
    
class UserCompanyDepartment(models.Model):
    user=models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='user_access'
    )

    company=models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        related_name='company_access'
    )

    department=models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='department_access'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company', 'department')
        verbose_name = "Vínculo Usuário , Empresa e Departamento"
        verbose_name_plural = "Vínculo Usuário , Empresa e Departamento"