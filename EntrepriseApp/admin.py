from django.contrib import admin
from .models import Utilisateur, Entreprise

class UserAdmin(admin.ModelAdmin):
    #modifier l'affichage des champs dans l'interface d'administration
    list_display = ('username', 'email','is_active','is_supperuser')
    #en peut changer les champs modifiable dans l'interface d'administration
    list_editable=('username','is_active','is_supperuser')
    #pour ajouter une zone de recherche dans l'interface d'administration
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_supperuser','role')
    #ell nous permet de voir qu'est ce qu'on a des user
    list_per_page = 1
admin.site.register(Utilisateur)
admin.site.register(Entreprise)

