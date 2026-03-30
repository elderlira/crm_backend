from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, Department, Role

# 1. Registros Simples (Apenas uma vez para cada)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Role)

# 2. Configuração customizada do Usuário
class CustomUserAdmin(UserAdmin):
    # Campos que aparecem na lista de usuários
    list_display = ('username', 'email', 'company', 'department', 'role', 'is_staff')
    
    # Adiciona os campos novos nos formulários de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Corporativas', {
            'fields': ('company', 'department', 'role'),
        }),
    )

    # Adiciona os campos no formulário de criação (quando você clica em "Add User")
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Corporativas', {
            'fields': ('company', 'department', 'role'),
        }),
    )

# 3. Registro final do Usuário com a classe customizada
admin.site.register(User, CustomUserAdmin)