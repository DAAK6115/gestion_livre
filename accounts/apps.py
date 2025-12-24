from django.apps import AppConfig
import os


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.contrib.auth import get_user_model

        superusers = os.environ.get("DJANGO_SUPERUSERS")
        if not superusers:
            return

        User = get_user_model()

        for entry in superusers.split(","):
            try:
                username, password, email = entry.split(":")
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    print(f"[AUTO] Superuser {username} created")
            except Exception as e:
                print("[AUTO] Superuser error:", e)
