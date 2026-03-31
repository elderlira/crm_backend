# No arquivo createuser.py
from django.core.management.base import BaseCommand
from authentication.models import User, Role

class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input("E-mail (Login): ")
        username = input("Username: ")
        password = input("Senha: ")

        try:
            # BUSQUE PELO ID 1 (que é o seu Admin na imagem)
            role_admin = Role.objects.get(id=1) 
            
            user = User.objects.create_superuser(
                email=email,
                username=username,
                password=password,
                role=role_admin # Atribui a role de Admin
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuário {username} criado com sucesso!'))
        
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR('Erro: A Role com ID 1 não foi encontrada no banco.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {e}'))