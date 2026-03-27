from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "Create a normal user"

    def handle(self, *args, **kwargs):

        email = input("Email: ")
        username = input("Username: ")
        password = input("Password: ")

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("User created successfully"))