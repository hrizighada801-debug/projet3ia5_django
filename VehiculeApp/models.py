from django.db import models
class Offre(models.Model):
    immatricule = models.CharField(max_length=20, unique=True)
    type_vehiciule = models.CharField(max_length=50, choices=[('camion', 'Camion'), ('voiture', 'Voiture'), ('moto', 'Moto')])
    capacite_kg = models.IntegerField()
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#il faut le verifier 
    
