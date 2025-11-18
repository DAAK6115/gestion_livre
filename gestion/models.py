from django.db import models
from django.utils import timezone


class Centre(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    ville = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Ex: COMPAGNON_180"
    )
    nom = models.CharField(
        max_length=100,
        help_text="Ex: Compagnon"
    )
    pages = models.PositiveIntegerField(default=0)
    prix_unitaire_defaut = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Prix par défaut (peut être modifié par centre/période)."
    )

    def __str__(self):
        return f"{self.nom} ({self.pages} p.)"


class ReleveCentreLivre(models.Model):
    PERIODE_SEMAINE = "WEEK"
    PERIODE_MOIS = "MONTH"
    PERIODE_ANNEE = "YEAR"

    PERIODE_CHOICES = (
        (PERIODE_SEMAINE, "Semaine"),
        (PERIODE_MOIS, "Mois"),
        (PERIODE_ANNEE, "Année"),
    )

    centre = models.ForeignKey(
        Centre,
        on_delete=models.CASCADE,
        related_name="releves"
    )
    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name="releves"
    )

    # Type de période : semaine / mois / année
    type_periode = models.CharField(
        max_length=10,
        choices=PERIODE_CHOICES
    )

    # Période couverte par ce relevé
    date_debut = models.DateField()
    date_fin = models.DateField()

    # Données métiers (équivalent à tes colonnes Excel)
    quantite_recue = models.PositiveIntegerField(default=0)
    quantite_vendue = models.PositiveIntegerField(default=0)
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Prix appliqué sur cette période."
    )
    depenses = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Dépenses liées (transport, commissions...)."
    )

    # Champs calculés
    montant_ventes = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        default=0
    )
    quantite_reste = models.IntegerField(
        editable=False,
        default=0
    )

    # Pour traçabilité
    cree_le = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Relevé centre / livre"
        verbose_name_plural = "Relevés centre / livre"
        unique_together = (
            "centre",
            "livre",
            "type_periode",
            "date_debut",
            "date_fin",
        )

    def __str__(self):
        return f"{self.centre} - {self.livre} ({self.date_debut} → {self.date_fin})"

    @property
    def trimestre(self):
        """
        Permet les rapports par trimestre :
        Q1 = mois 1-3, Q2 = 4-6, etc.
        """
        mois = self.date_fin.month
        return (mois - 1) // 3 + 1

    def save(self, *args, **kwargs):
        # Si aucun prix renseigné, on reprend celui du livre
        if not self.prix_unitaire and self.livre_id:
            self.prix_unitaire = self.livre.prix_unitaire_defaut

        # Calcul automatique montant & reste
        self.montant_ventes = self.quantite_vendue * self.prix_unitaire
        self.quantite_reste = self.quantite_recue - self.quantite_vendue

        super().save(*args, **kwargs)
