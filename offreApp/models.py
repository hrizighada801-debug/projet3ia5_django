from django.db import models
class Offre(models.Model):
    Vehicules = models.ForeignKey('Vehiculess.vehicules', on_delete=models.CASCADE, related_name='offres')
    expedition = models.ForeignKey('ExpeditionApp.Expedition', on_delete=models.CASCADE, related_name='offres')
    transporteur = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, related_name='offres')
    prix = models.DecimalField()
    delai_jours = models.PositiveIntegerField()
    statut = models.CharField(max_length=20, choices=[('p','proposee'),('a', 'acceptee'), ('r', 'refusee'), ('r', 'retiree')], default='proposee')
    date_proposition = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
