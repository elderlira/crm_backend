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
