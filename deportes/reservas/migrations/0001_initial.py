import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ActividadDeportiva",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("descripcion", models.TextField(blank=True)),
                ("lugar", models.CharField(max_length=150)),
                (
                    "cupo",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
            ],
            options={
                "verbose_name": "actividad deportiva",
                "verbose_name_plural": "actividades deportivas",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="Horario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dia",
                    models.CharField(
                        choices=[
                            ("LUN", "Lunes"),
                            ("MAR", "Martes"),
                            ("MIE", "Miércoles"),
                            ("JUE", "Jueves"),
                            ("VIE", "Viernes"),
                            ("SAB", "Sábado"),
                            ("DOM", "Domingo"),
                        ],
                        max_length=3,
                    ),
                ),
                ("hora_inicio", models.TimeField()),
                ("hora_fin", models.TimeField()),
                (
                    "actividad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="horarios",
                        to="reservas.actividaddeportiva",
                    ),
                ),
            ],
            options={
                "verbose_name": "horario",
                "verbose_name_plural": "horarios",
                "ordering": ["actividad", "dia", "hora_inicio"],
            },
        ),
        migrations.CreateModel(
            name="Inscripcion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=50)),
                ("apellido", models.CharField(max_length=50)),
                (
                    "dni",
                    models.CharField(
                        max_length=8,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^\\d{7,8}$", "El DNI debe tener 7 u 8 dígitos."
                            )
                        ],
                    ),
                ),
                ("fecha_inscripcion", models.DateField(auto_now_add=True)),
                (
                    "estado",
                    models.CharField(
                        choices=[("ACTIVA", "Activa"), ("CANCELADA", "Cancelada")],
                        default="ACTIVA",
                        max_length=9,
                    ),
                ),
                (
                    "horario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inscripciones",
                        to="reservas.horario",
                    ),
                ),
            ],
            options={
                "verbose_name": "inscripción",
                "verbose_name_plural": "inscripciones",
                "ordering": ["apellido", "nombre"],
            },
        ),
        migrations.AddConstraint(
            model_name="horario",
            constraint=models.CheckConstraint(
                condition=models.Q(("hora_fin__gt", models.F("hora_inicio"))),
                name="hora_fin_posterior_a_hora_inicio",
            ),
        ),
        migrations.AddConstraint(
            model_name="horario",
            constraint=models.UniqueConstraint(
                fields=("actividad", "dia", "hora_inicio"),
                name="horario_unico_por_actividad",
            ),
        ),
        migrations.AddConstraint(
            model_name="inscripcion",
            constraint=models.UniqueConstraint(
                fields=("dni", "horario"), name="inscripcion_unica_por_horario"
            ),
        ),
    ]
