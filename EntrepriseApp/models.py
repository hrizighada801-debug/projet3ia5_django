from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
#fonction pour la validation de l'email + il faut faire l'app
def validate_email(value):
    if not value:
        raise ValidationError('L\'adresse e-mail doit etre obligatoire')
    if not value.endswith('@gmail.com'):
        raise ValidationError('le domaine accepté est gmail')
matricule_fiscale_validator =RegexValidator(regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$', message="Le format du matricule fiscale est invalide. Il doit être au format 1234567/A/B/C/123.") 
class Utilisateur(AbstractUser):
    # Ajoutez des champs supplémentaires si nécessaire
    user_id=models.CharField(primary_key=True,max_length=8)
    #l'app de fonction de validation de l'email
    email = models.EmailField(unique=True, validators=[validate_email])

    telephone = models.CharField(max_length=15, blank=True, null=True)
    role=models.CharField(max_length=20, choices=[('admin', 'Admin'), ('c', 'Chargeur'),('t', 'Transporteur')], default='c')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200, blank=False, null=False)
    matricule_fiscale = models.CharField(max_length=17, unique=True,validators=[matricule_fiscale_validator])

    adresse = models.TextField(validators=[MinLengthValidator(20,"L'adresse ne peut pas voir moins de 20 charactères")])

    type_entreprise = models.CharField(max_length=100, choices=[('c', 'Chargeur'), ('t', 'Transporteur')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')