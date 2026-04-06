from django.db import models


class Department(models.Model):

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(max_length=255)

    message = models.TextField(
        blank=True,
        null=True
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_department_per_company"
            )
        ]

    def __str__(self):
        return f"{self.company.name} - {self.name}"


class DepartmentUser(models.Model):

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_departments"
    )

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="department_users"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "department"],
                name="unique_user_department"
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.department.name}"