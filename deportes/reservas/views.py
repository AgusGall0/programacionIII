from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActividadDeportivaForm
from .models import ActividadDeportiva


@login_required
@permission_required('reservas.view_actividaddeportiva', raise_exception=True)
def lista_actividades(request):
    actividades = ActividadDeportiva.objects.all()
    return render(request, 'reservas/lista_actividades.html', {'actividades': actividades})


@login_required
@permission_required('reservas.view_actividaddeportiva', raise_exception=True)
def detalle_actividad(request, actividad_id):
    actividad = get_object_or_404(ActividadDeportiva, pk=actividad_id)
    horarios = actividad.horarios.all()
    return render(request, 'reservas/detalle_actividad.html', {
        'actividad': actividad,
        'horarios': horarios,
    })


@login_required
@permission_required('reservas.add_actividaddeportiva', raise_exception=True)
def agregar_actividad(request):
    if request.method == 'POST':
        form = ActividadDeportivaForm(request.POST)
        if form.is_valid():
            actividad = form.save()
            messages.success(request, f'La actividad "{actividad.nombre}" se registró correctamente.')
            return redirect('reservas:agregar_actividad')
        messages.error(request, 'No se pudo registrar la actividad. Revisá los datos ingresados.')
    else:
        form = ActividadDeportivaForm()
    return render(request, 'reservas/agregar_actividad.html', {'form': form})
