from django.db import models

class Label(models.Model):
    label = models.CharField(max_length=100, verbose_name="Etiqueta")
    color = models.CharField(max_length=7, verbose_name="Cor (Hexadecimal)")
    online = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} )"
    
    class Meta:
        verbose_name = "label"
        verbose_name_plural = "label"