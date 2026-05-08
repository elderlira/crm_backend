from django.db import models

class Permission(models.Model):
  
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Permissão"
        verbose_name_plural = "Permissões"
        ordering = ['label']