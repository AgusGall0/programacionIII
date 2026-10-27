from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'reservas'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='reservas:lista_actividades'), name='inicio'),
    path('actividades/', views.lista_actividades, name='lista_actividades'),
    path('actividades/agregar/', views.agregar_actividad, name='agregar_actividad'),
    path('actividades/<int:actividad_id>/', views.detalle_actividad, name='detalle_actividad'),
]
