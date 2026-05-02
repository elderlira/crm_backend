from django.db import models

class Label(models.Model):
    label = models.CharField(max_length=100, verbose_name="Etiqueta")
    color = models.CharField(max_length=7, verbose_name="Hexadecimal")
    online = models.BooleanField(default=True)

    company = models.ForeignKey(
        'companies.Company', 
        on_delete=models.CASCADE, 
        related_name='labels',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.label} ({self.company.name})"
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"