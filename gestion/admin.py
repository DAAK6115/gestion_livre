from django.contrib import admin
from .models import Centre, Livre, ReleveCentreLivre


@admin.register(Centre)
class CentreAdmin(admin.ModelAdmin):
    list_display = ("nom", "ville", "contact")
    search_fields = ("nom", "ville")


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ("nom", "code", "pages", "prix_unitaire_defaut")
    search_fields = ("nom", "code")


@admin.register(ReleveCentreLivre)
class ReleveCentreLivreAdmin(admin.ModelAdmin):
    list_display = (
        "centre",
        "livre",
        "type_periode",
        "date_debut",
        "date_fin",
        "quantite_vendue",
        "montant_ventes",
    )
    list_filter = ("type_periode", "centre", "livre", "date_debut", "date_fin")
    search_fields = ("centre__nom", "livre__nom")
