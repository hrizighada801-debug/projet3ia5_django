from django.contrib import admin
from .models import Utilisateur, Entreprise
from VehiculeApp.models import Vehicule

class UserAdmin(admin.ModelAdmin):
    #modifier l'affichage des champs dans l'interface d'administration
    list_display = ('username', 'email','is_active','is_superuser')
    #en peut changer les champs modifiable dans l'interface d'administration
    list_editable=('is_active',)
    #pour ajouter une zone de recherche dans l'interface d'administration
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_superuser','role')
    #ell nous permet de voir qu'est ce qu'on a des user
    list_per_page = 1
class VehiculeInline(admin.TabularInline):
    model = Vehicule
    extra = 0
    fields = (
        'immatriculation',
        'type_vehicule',
        'capacite_kg',
        'disponible',
    )

admin.site.register(Utilisateur, UserAdmin)

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    search_fields = ('raison_sociale',)
    inlines = [VehiculeInline]

