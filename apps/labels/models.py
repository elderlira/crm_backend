from django.db import models

class Label(models.Model):
    etiqueta = models.CharField(max_length=100, verbose_name="Etiqueta")
    cor = models.CharField(max_length=7, verbose_name="Cor (Hexadecimal)")
    online = models.BooleanField(default=True)

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='labels'  
    )

    def __str__(self):
        return f"{self.etiqueta} ({self.company.name})"
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"