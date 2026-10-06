from datetime import timezone
from django.core.exceptions import ValidationError
from django.db import models
#app de bib 
from django.core.validators import  MinValueValidator
class Expedition(models.Model):
    reference = models.CharField(max_length=100, unique=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    #valeur positive pour le poids
    poids_kg = models.DecimalField(validators=[MinValueValidator(0)])
    date_souhaitee = models.DateField()
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=[('b', 'publiee'), ('a', 'attribuee'), ('e', 'En cours'), ('l', 'livree'),('an','annuler')], default='publies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey('EntrepriseApp.entreprise', on_delete=models.CASCADE, related_name='expeditions')
    #validation entre deux valeur
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'c':
            raise ValidationError("L'entreprise associée doit être de type 'Chargeur'.")

    
    #cls: c'est un objet 
    def _generate_reference(cls):
        annee = timezone.now().strftime('%Y')
        prefixe = f"EXP_{annee}_"
        dernier= cls.objects.filter(reference__startswith=prefixe).order_by('-reference').last()
        compteur = int(dernier.reference[-5:]) + 1 if dernier else 1
        if compteur > 99999:
            raise ValueError("Le compteur a dépassé la limite de 99999.")
        return f"{prefixe}{compteur:05d}"
# "update w2la insert  
    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        self.full_clean()  # Appel de la méthode full_clean pour valider les champs avant l'enregistrement
        super().save(*args, **kwargs)