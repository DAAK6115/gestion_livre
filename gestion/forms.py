# gestion/forms.py
from django import forms
from .models import ReleveCentreLivre, Livre, Centre


from django import forms
from .models import ReleveCentreLivre, Livre, Centre


from django import forms
from .models import ReleveCentreLivre, Centre


class ReleveCentreLivreForm(forms.ModelForm):
    class Meta:
        model = ReleveCentreLivre
        fields = [
            "centre",
            "livre",
            "date_debut",
            "date_fin",
            "quantite_recue",
            "quantite_vendue",
            "prix_unitaire",
            "depenses",
            "operateur_mobile_money",
            "taux_frais_retrait",
        ]
        labels = {
            "centre": "Centre",
            "livre": "Livre",
            "date_debut": "Date de début",
            "date_fin": "Date de fin",
            "quantite_recue": "Nombre de livres en stock / reçus pour la période",
            "quantite_vendue": "Nombre de livres vendus pendant la période",
            "prix_unitaire": "Prix unitaire (FCFA)",
            "depenses": "Autres dépenses (transport, commissions, …)",
            "operateur_mobile_money": "Opérateur Mobile Money",
            "taux_frais_retrait": "Taux de frais de retrait (%)",
        }
        widgets = {
            "centre": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                }
            ),
            "livre": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                }
            ),
            "date_debut": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                }
            ),
            "date_fin": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                }
            ),
            "quantite_recue": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "min": 0,
                }
            ),
            "quantite_vendue": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "min": 0,
                }
            ),
            "prix_unitaire": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "min": 0,
                    "step": "0.01",
                }
            ),
            "depenses": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "min": 0,
                    "step": "0.01",
                }
            ),
            "operateur_mobile_money": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                }
            ),
            "taux_frais_retrait": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "Ex : 1.5 pour 1,5%",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si l'utilisateur est un centre, on fixe son centre et on le bloque
        if user and hasattr(user, "is_centre") and user.is_centre() and user.centre_id:
            self.fields["centre"].queryset = Centre.objects.filter(pk=user.centre_id)
            self.fields["centre"].initial = user.centre
            self.fields["centre"].disabled = True




class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ["code", "nom", "pages", "prix_unitaire_defaut"]
        labels = {
            "code": "Code",
            "nom": "Nom",
            "pages": "Nombre de pages",
            "prix_unitaire_defaut": "Prix unitaire par défaut (FCFA)",
        }
        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "placeholder": "COMPAGNON_180",
                }
            ),
            "nom": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "placeholder": "Compagnon",
                }
            ),
            "pages": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "min": 0,
                }
            ),
            "prix_unitaire_defaut": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "step": "0.01",
                    "min": 0,
                }
            ),
        }


class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = ["nom", "ville", "contact"]
        labels = {
            "nom": "Nom du centre",
            "ville": "Ville",
            "contact": "Contact",
        }
        widgets = {
            "nom": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "placeholder": "ABOBO, YAMOUSSOKRO...",
                }
            ),
            "ville": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "placeholder": "Abidjan, Bouaké...",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900",
                    "placeholder": "Nom / téléphone / email",
                }
            ),
        }
