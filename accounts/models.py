from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = "ADMIN"
    ROLE_CENTRE = "CENTRE"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Administrateur"),
        (ROLE_CENTRE, "Centre"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_CENTRE,
    )

    # centre = null pour un admin, rempli pour un utilisateur "centre"
    centre = models.ForeignKey(
        "gestion.Centre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="utilisateurs",
    )

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_centre(self):
        return self.role == self.ROLE_CENTRE
