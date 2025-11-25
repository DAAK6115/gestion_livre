from django.db import models
from django.utils import timezone
from decimal import Decimal



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
        # Mobile Money
    OPERATEUR_MTN = "MTN"
    OPERATEUR_ORANGE = "ORANGE"
    OPERATEUR_MOOV = "MOOV"
    OPERATEUR_WAVE = "WAVE"

    OPERATEUR_CHOICES = (
        (OPERATEUR_MTN, "MTN Money"),
        (OPERATEUR_ORANGE, "Orange Money"),
        (OPERATEUR_MOOV, "Moov Money"),
        (OPERATEUR_WAVE, "Wave"),
    )

    operateur_mobile_money = models.CharField(
        max_length=10,
        choices=OPERATEUR_CHOICES,
        blank=True,
        null=True,
        help_text="Opérateur mobile money utilisé pour encaisser / retirer l'argent.",
    )

    taux_frais_retrait = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=(
            "Taux des frais de retrait en %. Exemple : 1.5 pour 1,5%. "
            "Si laissé vide, il sera calculé automatiquement selon l'opérateur."
            ),
    )

    montant_frais_retrait = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        editable=False,
        help_text="Frais de retrait calculés automatiquement à partir du taux.",
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

        @property
        def trimestre(self):
            mois = self.date_fin.month
            return (mois - 1) // 3 + 1

    def _compute_mobile_money_fees(self):
        """
        Calcule automatiquement les frais de retrait selon l'opérateur.
        Règles (simplifiées) basées sur ce que tu as donné :
          - ORANGE : 1% du montant retiré
          - MOOV   : 1% du montant retiré
          - WAVE   : 0% (retrait gratuit)
          - MTN    :
              * < 100 000 FCFA  -> 0 frais
              * 100 000 à 500 000 -> 1%
              * > 500 000 -> 5 000 FCFA (on enregistre aussi un taux effectif)
        Retourne (frais, taux_en_pourcentage_ou_None)
        """
        montant = self.montant_ventes or Decimal("0")
        if not self.operateur_mobile_money or montant <= 0:
            return Decimal("0"), None

        op = self.operateur_mobile_money

        # Orange & Moov : 1%
        if op in (self.OPERATEUR_ORANGE, self.OPERATEUR_MOOV):
            taux = Decimal("1.00")
            frais = (montant * taux / Decimal("100")).quantize(Decimal("0.01"))
            return frais, taux

        # Wave : 0%
        if op == self.OPERATEUR_WAVE:
            taux = Decimal("0.00")
            frais = Decimal("0.00")
            return frais, taux

        # MTN : règles spéciales
        if op == self.OPERATEUR_MTN:
            if montant < Decimal("100000"):
                # Pas de frais sous 100 000
                return Decimal("0.00"), Decimal("0.00")
            elif montant <= Decimal("500000"):
                # 1% entre 100 000 et 500 000
                taux = Decimal("1.00")
                frais = (montant * taux / Decimal("100")).quantize(Decimal("0.01"))
                return frais, taux
            else:
                # > 500 000 : 5 000 FCFA fixe, on calcule aussi un taux effectif
                frais = Decimal("5000.00")
                if montant > 0:
                    taux = (frais * Decimal("100") / montant).quantize(Decimal("0.01"))
                else:
                    taux = None
                return frais, taux

        # Par défaut si jamais un autre opérateur arrive
        return Decimal("0"), None

    def save(self, *args, **kwargs):
        # Si aucun prix renseigné, on reprend celui du livre
        if not self.prix_unitaire and self.livre_id:
            self.prix_unitaire = self.livre.prix_unitaire_defaut

        # Calcul automatique montant & reste
        self.montant_ventes = self.quantite_vendue * self.prix_unitaire
        self.quantite_reste = self.quantite_recue - self.quantite_vendue

        # Frais de retrait Mobile Money
        if not self.taux_frais_retrait and self.operateur_mobile_money:
            # Aucun taux saisi → on applique automatiquement les règles
            frais, taux = self._compute_mobile_money_fees()
            self.montant_frais_retrait = frais
            if taux is not None:
                self.taux_frais_retrait = taux
        elif self.taux_frais_retrait:
            # Taux saisi manuellement → on respecte ce choix
            self.montant_frais_retrait = (
                self.montant_ventes * self.taux_frais_retrait / Decimal("100")
            )
        else:
            # Pas d'opérateur ni de taux → pas de frais
            self.montant_frais_retrait = Decimal("0.00")

        super().save(*args, **kwargs)
