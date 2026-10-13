from django.contrib import admin
from .models import Vehicule
#c'est la dexiéme facon pour enregistrer un model dans l'interface d'administration
#c'est décorateur
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatricule', 'type_vehicule', 'capacite_kg', 'disponibilite', 'Entreprise')
  
  
  
  #fieldsets = (

        #('Identification', {

         #   'fields': ('immatriculation', 'type_vehicule', 'capacite_kg')

       # }),

      # "" ('Statut et rattachement', {

          #  'fields': ('disponible', 'entreprise')

     #   }),

       # ('Horodatage', {

          #  'fields': ('created_at', 'updated_at'),

          # "" 'classes': ('collapse',),

       # }),

    
 