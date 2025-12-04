from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Create or update a default superuser based on env vars."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin12345")

        user, created = User.objects.get_or_create(username=username, defaults={
            "email": email,
        })

        # On s'assure qu'il est bien admin + on met à jour le password
        user.is_staff = True
        user.is_superuser = True
        user.email = email
        user.set_password(password)
        user.save()

        if created:
            msg = f"Superuser '{username}' created."
        else:
            msg = f"Superuser '{username}' updated."

        self.stdout.write(self.style.SUCCESS(msg))
