from django import forms

from .models import ActividadDeportiva


class ActividadDeportivaForm(forms.ModelForm):
    class Meta:
        model = ActividadDeportiva
        fields = ['nombre', 'descripcion', 'lugar', 'cupo']
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'lugar': 'Lugar',
            'cupo': 'Cupo',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'cupo': forms.NumberInput(attrs={'min': 1}),
        }
        error_messages = {
            'nombre': {'unique': 'Ya existe una actividad con ese nombre.'},
        }
