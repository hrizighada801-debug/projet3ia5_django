from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class Offre(models.Model):
    Vehicules = models.ForeignKey(
        'VehiculeApp.Vehicule',
        on_delete=models.CASCADE,
        related_name='offres'
    )

    expedition = models.ForeignKey(
        'ExpeditionApp.Expedition',
        on_delete=models.CASCADE,
        related_name='offres'
    )

    transporteur = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='offres'
    )

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    statut = models.CharField(
        max_length=20,
        choices=[
            ('p', 'proposee'),
            ('a', 'acceptee'),
            ('ref', 'refusee'),
            ('r', 'retiree')
        ],
        default='proposee'
    )

    date_proposition = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        # Regle 1 : l'entreprise associée doit être un transporteur
        if self.transporteur_id and self.transporteur.type_entreprise != 't':
            raise ValidationError(
                "L'entreprise associée doit être de type 'Transporteur'."
            )

        # Regle 2 : le véhicule doit appartenir au transporteur
        if self.Vehicules_id and self.transporteur_id:
            if self.Vehicules.entreprise != self.transporteur:
                raise ValidationError(
                    "Le véhicule doit appartenir à l'entreprise "
                    "transporteur associée à l'offre."
                )

        # Regle 3 : l'expédition doit être publiée
        if self.expedition_id and self.expedition.statut != 'b':
            raise ValidationError(
                "L'expédition associée doit être publiée."
            )

        # Regle 4 : une seule offre proposée par transporteur et expédition
        if self.transporteur_id and self.expedition_id:
            offres_existantes = Offre.objects.filter(
                transporteur_id=self.transporteur_id,
                expedition_id=self.expedition_id,
                statut='p'
            ).exclude(pk=self.pk)

            if offres_existantes.exists():
                raise ValidationError(
                    "Cette entreprise a déjà proposé une offre "
                    "pour cette expédition."
                )

