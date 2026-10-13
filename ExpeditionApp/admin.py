
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from offreApp.models import Offre
from .models import Expedition


class EnRetardFilter(admin.SimpleListFilter):
    title = 'En retard'
    parameter_name = 'en_retard'

    def lookups(self, request, model_admin):
        return (
            ('oui', 'Oui'),
            ('non', 'Non'),
        )

    def queryset(self, request, queryset):
        en_retard = queryset.filter(
            statut='b',
            date_souhaitee__lt=timezone.localdate(),
        )

        if self.value() == 'oui':
            return en_retard

        if self.value() == 'non':
            return queryset.exclude(pk__in=en_retard.values('pk'))

        return queryset
class OffreInline(admin.StackedInline):
    model = Offre
    fk_name = 'expedition'
    extra = 0

    fields = (
        'transporteur',
        'Vehicules',
        'prix',
        'delai_jours',
        'statut',
    )

    readonly_fields = (
        'transporteur',
        'Vehicules',
        'prix',
        'delai_jours',
        'statut',
    )

    show_change_link = True
    can_delete = False


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'entreprise',
        'ville_depart',
        'ville_arrivee',
        'statut',
        'statut_colore',
        'date_souhaitee',
    )
    inlines = [OffreInline]
    list_filter = (
        'statut',
        'ville_depart',
        EnRetardFilter,
    )

    search_fields = (
        'reference',
        'ville_depart',
        'ville_arrivee',
        'entreprise__raison_sociale',
    )

    list_editable = ('statut',)
    ordering = ('-created_at',)
    date_hierarchy = 'date_souhaitee'
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')

    autocomplete_fields = ('entreprise',)

    fieldsets = (
        ('Informations de l’expédition', {
            'fields': (
                'reference',
                'entreprise',
                'ville_depart',
                'ville_arrivee',
                'poids_kg',
                'description',
            )
        }),
        ('Planification', {
            'fields': ('date_souhaitee', 'statut')
        }),
        ('Dates système', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'b': '#F0AD4E',
            'a': '#5CB85C',
            'e': '#337AB7',
            'l': '#398439',
            'an': '#D9534F',
        }

        return format_html(
            '<span style="color:white;background:{};'
            'padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#777777'),
            obj.get_statut_display(),
        )
