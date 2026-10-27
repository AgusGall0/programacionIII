from django.contrib.auth.management import create_permissions
from django.db import migrations

ROLES = {
    'Administrador': {
        'actividaddeportiva': ['add', 'change', 'delete', 'view'],
        'horario': ['add', 'change', 'delete', 'view'],
        'inscripcion': ['add', 'change', 'delete', 'view'],
    },
    'Coordinador': {
        'actividaddeportiva': ['add', 'change', 'view'],
        'horario': ['add', 'change', 'view'],
        'inscripcion': ['change', 'view'],
    },
    'Socio': {
        'actividaddeportiva': ['view'],
        'horario': ['view'],
    },
}


def crear_roles(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    for nombre, modelos in ROLES.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        codenames = [
            f'{accion}_{modelo}'
            for modelo, acciones in modelos.items()
            for accion in acciones
        ]
        permisos = Permission.objects.filter(
            content_type__app_label='reservas',
            codename__in=codenames,
        )
        grupo.permissions.set(permisos)


def eliminar_roles(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=ROLES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_roles, eliminar_roles),
    ]
