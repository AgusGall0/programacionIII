from django.contrib import admin
from django.db.models import Count

from .models import ActividadDeportiva, Horario, Inscripcion

admin.site.site_header = 'Administración de Deportes Unca'
admin.site.site_title = 'Deportes Unca'
admin.site.index_title = 'Gestión de actividades deportivas'


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1


@admin.register(ActividadDeportiva)
class ActividadDeportivaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'lugar', 'cupo', 'cantidad_horarios']
    list_display_links = ['nombre']
    list_editable = ['cupo']
    list_filter = ['lugar']
    search_fields = ['nombre', 'lugar', 'descripcion']
    ordering = ['nombre']
    list_per_page = 20
    inlines = [HorarioInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total_horarios=Count('horarios'))

    @admin.display(description='Horarios', ordering='total_horarios')
    def cantidad_horarios(self, obj):
        return obj.total_horarios


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['actividad', 'dia', 'hora_inicio', 'hora_fin']
    list_filter = ['actividad', 'dia']
    search_fields = ['actividad__nombre', 'actividad__lugar']
    list_select_related = ['actividad']
    autocomplete_fields = ['actividad']


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'horario', 'estado', 'fecha_inscripcion']
    list_filter = ['estado', 'horario__actividad', 'fecha_inscripcion']
    search_fields = ['apellido', 'nombre', 'dni', 'horario__actividad__nombre']
    list_select_related = ['horario__actividad']
    autocomplete_fields = ['horario']
    readonly_fields = ['fecha_inscripcion']
    date_hierarchy = 'fecha_inscripcion'
    actions = ['cancelar_inscripciones']

    @admin.action(description='Cancelar las inscripciones seleccionadas', permissions=['change'])
    def cancelar_inscripciones(self, request, queryset):
        cantidad = queryset.update(estado=Inscripcion.Estado.CANCELADA)
        self.message_user(request, f'Se cancelaron {cantidad} inscripción(es).')
