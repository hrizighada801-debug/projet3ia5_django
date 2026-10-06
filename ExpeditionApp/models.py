from django.db import models
class Expedition(models.Model):
    reference = models.CharField(max_length=100, unique=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField()
    date_souhaitee = models.DateField()
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=[('b', 'publiee'), ('a', 'attribuee'), ('e', 'En cours'), ('l', 'livree'),('a','annuler')], default='publies')

    
    
    
    
    entreprise = models.ForeignKey('EntrepriseApp.entreprise', on_delete=models.CASCADE, related_name='expeditions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
