from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Tabela company_departments (Relação entre Empresa e Departamentos)
class CompanyDepartment(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('company', 'department')