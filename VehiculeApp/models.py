from django.db import models
from django.core.exceptions import ValidationError


class Vehicule(models.Model):
    TYPES_VEHICULE = [
        ('camionnette', 'Camionnette / utilitaire léger'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur', 'Camion porteur'),
        ('semi_remorque', 'Semi-remorque'),
    ]

    immatriculation = models.CharField(
        max_length=20,
        unique=True
    )

    type_vehicule = models.CharField(
        max_length=30,
        choices=TYPES_VEHICULE
    )

    capacite_kg = models.PositiveIntegerField()

    disponible = models.BooleanField(default=True)

    entreprise = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='vehicules'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.entreprise_id and self.entreprise.type_entreprise != 't':
            raise ValidationError(
                "Le véhicule doit appartenir à une entreprise transporteur."
            )

    def __str__(self):
        return self.immatriculation
