
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import Offre


@admin.action(description="Exporter la sélection en CSV")
def exporter_offres_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        'attachment; filename="offres.csv"'
    )

    response.write('\ufeff')
    writer = csv.writer(response)

    writer.writerow([
        'reference_expedition',
        'transporteur',
        'prix',
        'statut',
    ])

    for offre in queryset.select_related(
        'expedition',
        'transporteur',
    ):
        writer.writerow([
            offre.expedition.reference,
            offre.transporteur.raison_sociale,
            offre.prix,
            offre.get_statut_display(),
        ])

    return response


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = (
        'expedition',
        'transporteur',
        'Vehicules',
        'prix',
        'delai_jours',
        'statut_colore',
        'date_proposition',
    )

    list_filter = ('statut', 'date_proposition')

    search_fields = (
        'expedition__reference',
        'transporteur__raison_sociale',
        'Vehicules__immatriculation',
    )

    ordering = ('-date_proposition',)
    date_hierarchy = 'date_proposition'
    list_per_page = 25

    autocomplete_fields = (
        'expedition',
        'transporteur',
        'Vehicules',
    )

    readonly_fields = (
        'date_proposition',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Détails de l’offre', {
            'fields': (
                'expedition',
                'transporteur',
                'Vehicules',
            )
        }),
        ('Conditions', {
            'fields': ('prix', 'delai_jours')
        }),
        ('Suivi', {
            'fields': (
                'statut',
                'date_proposition',
                'created_at',
                'updated_at',
            )
        }),
    )

    actions = [exporter_offres_csv]

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'p': '#F0AD4E',
            'a': '#5CB85C',
            'ref': '#D9534F',
            'r': '#777777',
        }

        return format_html(
            '<span style="color:white;background:{};'
            'padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.statut, '#777777'),
            obj.get_statut_display(),
        )

    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields)

        if obj and obj.statut == 'a':
            base.extend(['prix', 'delai_jours'])

        return base

