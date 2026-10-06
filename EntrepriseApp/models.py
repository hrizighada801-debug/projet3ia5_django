from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator
class Utilisateur(AbstractUser):
    # Ajoutez des champs supplémentaires si nécessaire
    user_id=models.AutoField(primary_key=True,max_length=8)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role=models.CharField(max_length=20, choices=[('admin', 'Admin'), ('c', 'Chargeur'),('t', 'Transporteur')], default='c')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200, blank=False, null=False)
    matricule_fiscale = models.CharField(max_length=17, unique=True)

    adresse = models.TextField(validators=[MinLengthValidator(400,"L'adresse ne peut pas voir moins de 20 charactères")])

    type_entreprise = models.CharField(max_length=100, choices=[('c', 'Chargeur'), ('t', 'Transporteur')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')