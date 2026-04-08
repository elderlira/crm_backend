import os
import sys
from django.core.management.base import BaseCommand

# Força o Python a incluir a pasta raiz no PATH de busca de módulos
sys.path.append(os.path.join(os.getcwd(), 'apps'))

try:
    # Tenta importar com o prefixo completo primeiro
    from apps.users.models import User
except ImportError:
    # Se falhar (dependendo de como o PYTHONPATH está no Mac), tenta direto
    from users.models import User

class Command(BaseCommand):
    help = 'Cria um superusuário inicial para o CRM'

    def handle(self, *args, **options):
        email = "admin@crm.com"
        username = "admin"
        password = "123456"

        try:
            if not User.objects.filter(email=email).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Usuário {email} criado com sucesso!'))
            else:
                self.stdout.write(self.style.WARNING(f'ℹ️ O usuário {email} já existe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro no banco de dados: {e}'))