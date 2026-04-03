from django.db import models

class ClosingReason(models.Model):

    reason = models.CharField(max_length=255)

    funnel = models.CharField(max_length=100)

    department = models.CharField(max_length=100)

    active = models.BooleanField(default=True)

    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason