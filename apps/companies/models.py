# apps/companies/models.py

from django.db import models


class Company(models.Model):

    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserCompany(models.Model):

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_companies"
    )

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="company_users"
    )

    profile = models.ForeignKey(
        "permissions.Profile",
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.company.name}"