from django.db import models

class Company(models.Model):
    name = models.CharField(max_length = 255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class CompanyDepartment(models.Model):
    company = models.ForeignKey(
        'company.Company', 
        on_delete=models.CASCADE, 
        related_name='company_departments'
    )
    department = models.ForeignKey(
        'departments.Department', 
        on_delete=models.CASCADE, 
        related_name='company_links'
    )

    class Meta:
        
        unique_together = ('company', 'department')
        verbose_name = "Departamento da Empresa"
        verbose_name_plural = "Departamentos das Empresas"

    def __str__(self):
        return f"{self.company.name} -> {self.department.name}"