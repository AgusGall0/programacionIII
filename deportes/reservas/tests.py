from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import ActividadDeportiva


class RolesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.actividad = ActividadDeportiva.objects.create(nombre='Fútbol', lugar='Polideportivo', cupo=22)
        cls.socio = cls.crear_usuario('socio', 'Socio')
        cls.coordinador = cls.crear_usuario('coordinador', 'Coordinador')
        cls.administrador = cls.crear_usuario('administrador', 'Administrador')

    @staticmethod
    def crear_usuario(username, rol):
        usuario = User.objects.create_user(username=username, password='clave-segura-123')
        usuario.groups.add(Group.objects.get(name=rol))
        return User.objects.get(pk=usuario.pk)

    def test_roles_creados_con_sus_permisos(self):
        permisos = {
            grupo.name: set(grupo.permissions.values_list('codename', flat=True))
            for grupo in Group.objects.all()
        }
        self.assertEqual(permisos['Socio'], {'view_actividaddeportiva', 'view_horario'})
        self.assertIn('add_actividaddeportiva', permisos['Coordinador'])
        self.assertNotIn('delete_actividaddeportiva', permisos['Coordinador'])
        self.assertEqual(len(permisos['Administrador']), 12)

    def test_rol_define_acceso_al_admin(self):
        self.assertFalse(self.socio.is_staff)
        self.assertTrue(self.coordinador.is_staff)
        self.assertTrue(self.administrador.is_staff)
        self.coordinador.groups.clear()
        self.coordinador.refresh_from_db()
        self.assertFalse(self.coordinador.is_staff)

    def test_anonimo_es_redirigido_al_login(self):
        respuesta = self.client.get(reverse('reservas:lista_actividades'))
        self.assertRedirects(respuesta, f"{reverse('login')}?next={reverse('reservas:lista_actividades')}")

    def test_socio_puede_ver_pero_no_agregar(self):
        self.client.force_login(self.socio)
        self.assertEqual(self.client.get(reverse('reservas:lista_actividades')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('reservas:detalle_actividad', args=[self.actividad.id])).status_code,
            200,
        )
        self.assertEqual(self.client.get(reverse('reservas:agregar_actividad')).status_code, 403)
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 302)

    def test_coordinador_puede_agregar_pero_no_eliminar_en_admin(self):
        self.client.force_login(self.coordinador)
        respuesta = self.client.post(reverse('reservas:agregar_actividad'), {
            'nombre': 'Vóley',
            'lugar': 'Gimnasio',
            'cupo': 12,
        })
        self.assertRedirects(respuesta, reverse('reservas:agregar_actividad'))
        self.assertTrue(ActividadDeportiva.objects.filter(nombre='Vóley').exists())
        url_eliminar = reverse('admin:reservas_actividaddeportiva_delete', args=[self.actividad.id])
        self.assertEqual(self.client.get(url_eliminar).status_code, 403)

    def test_administrador_puede_eliminar_en_admin(self):
        self.client.force_login(self.administrador)
        url_eliminar = reverse('admin:reservas_actividaddeportiva_delete', args=[self.actividad.id])
        self.client.post(url_eliminar, {'post': 'yes'})
        self.assertFalse(ActividadDeportiva.objects.filter(pk=self.actividad.pk).exists())


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superusuario = User.objects.create_superuser('admin', 'admin@unca.edu.ar', 'clave-segura-123')
        ActividadDeportiva.objects.create(nombre='Fútbol', lugar='Polideportivo', cupo=22)
        ActividadDeportiva.objects.create(nombre='Natación', lugar='Pileta', cupo=15)

    def setUp(self):
        self.client.force_login(self.superusuario)

    def test_list_display_muestra_los_campos(self):
        respuesta = self.client.get(reverse('admin:reservas_actividaddeportiva_changelist'))
        self.assertContains(respuesta, 'column-lugar')
        self.assertContains(respuesta, 'column-cupo')
        self.assertContains(respuesta, 'column-cantidad_horarios')

    def test_search_fields_filtra_por_lugar(self):
        respuesta = self.client.get(reverse('admin:reservas_actividaddeportiva_changelist'), {'q': 'pileta'})
        self.assertContains(respuesta, 'Natación')
        self.assertNotContains(respuesta, 'Fútbol')

    def test_paginas_del_admin_responden(self):
        for nombre in ('actividaddeportiva', 'horario', 'inscripcion'):
            for vista in ('changelist', 'add'):
                respuesta = self.client.get(reverse(f'admin:reservas_{nombre}_{vista}'))
                self.assertEqual(respuesta.status_code, 200)
