from django.core.management.base import BaseCommand
from authentication.models import User, Company, Role

class Command(BaseCommand):
    help = "Cria um usuário ADM inicial"

    def handle(self, *args, **kwargs):
        email = input("E-mail (Login): ")
        username = input("Username: ")
        password = input("Senha: ")

        # Pegamos a primeira empresa e a primeira role criadas no passo anterior
        company = Company.objects.first()
        role = Role.objects.get(name="ADM")

        if not company or not role:
            self.stdout.write(self.style.ERROR("Erro: Crie uma Empresa e a Role ADM no shell primeiro!"))
            return

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            company=company,
            role=role,
            is_staff=True,    # Para acessar o /admin do Django
            is_superuser=True # Para ter todos os poderes
        )

        self.stdout.write(self.style.SUCCESS(f"Usuário ADM {email} criado com sucesso!"))