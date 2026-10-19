from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class ActividadDeportiva(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    lugar = models.CharField(max_length=150)
    cupo = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'actividad deportiva'
        verbose_name_plural = 'actividades deportivas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    class Dia(models.TextChoices):
        LUNES = 'LUN', 'Lunes'
        MARTES = 'MAR', 'Martes'
        MIERCOLES = 'MIE', 'Miércoles'
        JUEVES = 'JUE', 'Jueves'
        VIERNES = 'VIE', 'Viernes'
        SABADO = 'SAB', 'Sábado'
        DOMINGO = 'DOM', 'Domingo'

    actividad = models.ForeignKey(
        ActividadDeportiva,
        on_delete=models.CASCADE,
        related_name='horarios',
    )
    dia = models.CharField(max_length=3, choices=Dia.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = 'horario'
        verbose_name_plural = 'horarios'
        ordering = ['actividad', 'dia', 'hora_inicio']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(hora_fin__gt=models.F('hora_inicio')),
                name='hora_fin_posterior_a_hora_inicio',
            ),
            models.UniqueConstraint(
                fields=['actividad', 'dia', 'hora_inicio'],
                name='horario_unico_por_actividad',
            ),
        ]

    def __str__(self):
        return (
            f'{self.actividad} - {self.get_dia_display()} '
            f'{self.hora_inicio:%H:%M} a {self.hora_fin:%H:%M}'
        )


class Inscripcion(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = 'ACTIVA', 'Activa'
        CANCELADA = 'CANCELADA', 'Cancelada'

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'^\d{7,8}$', 'El DNI debe tener 7 u 8 dígitos.'),
        ],
    )
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=9,
        choices=Estado.choices,
        default=Estado.ACTIVA,
    )
    horario = models.ForeignKey(
        Horario,
        on_delete=models.CASCADE,
        related_name='inscripciones',
    )

    class Meta:
        verbose_name = 'inscripción'
        verbose_name_plural = 'inscripciones'
        ordering = ['apellido', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['dni', 'horario'],
                name='inscripcion_unica_por_horario',
            ),
        ]

    def __str__(self):
        return f'{self.apellido}, {self.nombre} ({self.dni}) - {self.horario}'
