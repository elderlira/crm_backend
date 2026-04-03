from django.db import models


class Department(models.Model):
    
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name