# TP N° V – Creación del proyecto Django

Proyecto Django **deportes** con la aplicación **reservas**.

## 1.1 Entorno virtual

El entorno virtual se encuentra en la raíz del repositorio (`.venv/`, con el nombre `deportes`, que es el que aparece en el prompt al activarlo). No se sube al repositorio; se recrea con:

```bash
python3 -m venv .venv --prompt deportes
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r deportes/requirements.txt
```

## 1.2 Estructura del proyecto

```
deportes/
├── manage.py
├── deportes/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── reservas/
    ├── migrations/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    └── views.py
```

| Archivo | Función |
|---|---|
| `manage.py` | Utilidad de línea de comandos para administrar el proyecto: levantar el servidor (`runserver`), crear apps (`startapp`), generar y aplicar migraciones, crear superusuarios, etc. |
| `__init__.py` | Indica a Python que el directorio `deportes/` es un paquete. |
| `settings.py` | Configuración del proyecto: aplicaciones instaladas, base de datos, middleware, plantillas, idioma, zona horaria, archivos estáticos, `SECRET_KEY`, `DEBUG`, etc. |
| `urls.py` | Tabla de rutas principal: asocia cada URL con la vista que la atiende (o incluye las rutas de cada aplicación). |
| `asgi.py` | Punto de entrada para servidores compatibles con ASGI (asíncronos, p. ej. Uvicorn/Daphne). |
| `wsgi.py` | Punto de entrada para servidores compatibles con WSGI (síncronos, p. ej. Gunicorn), usado en producción. |

## 1.3 Intérprete en el editor

En `.vscode/settings.json` se configura VS Code para usar el intérprete `.venv/bin/python`. También se puede elegir manualmente con *Ctrl+Shift+P → Python: Select Interpreter*.

## 1.4 Aplicación reservas

Creada con `python manage.py startapp reservas` y registrada en `INSTALLED_APPS` de `deportes/settings.py`. Además se configuró el idioma (`es-ar`) y la zona horaria (`America/Argentina/Catamarca`).

## 1.5 Ejecución

```bash
cd deportes
python manage.py runserver
```

Luego abrir <http://127.0.0.1:8002/> en el navegador: se muestra la página de bienvenida de Django.

> Como los puertos 8000 y 8001 están ocupados, `manage.py` cambia el puerto por defecto de `runserver` a **8002**. Para usar otro: `python manage.py runserver 8003`.

---

# TP N° VIII – Admin de Django

## 1. Superusuario

```bash
cd deportes
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ingresar en <http://127.0.0.1:8002/admin/> con el usuario creado.

## 2. Modelos registrados

En `reservas/admin.py` se registran `ActividadDeportiva`, `Horario` e `Inscripcion` con `@admin.register`. Además se personalizan los títulos del sitio (`site_header`, `site_title`, `index_title`).

## 3. Operaciones desde el Admin

| Operación | Cómo |
|---|---|
| Listar | *Actividades deportivas* en el índice del Admin. |
| Crear | Botón **Agregar actividad deportiva**; los horarios se cargan en la misma pantalla (`HorarioInline`). |
| Actualizar | Clic en el nombre de la actividad, o editar el cupo directamente desde el listado (`list_editable`). |
| Eliminar | Botón **Eliminar** en el formulario, o la acción *Eliminar seleccionados* del listado. |

En inscripciones se agrega la acción *Cancelar las inscripciones seleccionadas*.

## 4. `list_display` y `search_fields`

| Modelo | `list_display` | `search_fields` |
|---|---|---|
| ActividadDeportiva | nombre, lugar, cupo, cantidad de horarios | nombre, lugar, descripción |
| Horario | actividad, día, hora de inicio, hora de fin | nombre y lugar de la actividad |
| Inscripcion | apellido, nombre, DNI, horario, estado, fecha | apellido, nombre, DNI, actividad |

También se usan `list_filter`, `ordering`, `list_per_page`, `list_select_related`, `autocomplete_fields`, `readonly_fields` y `date_hierarchy`.

## Seguridad

| Técnica | Implementación |
|---|---|
| Secretos fuera del código | `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` y `DJANGO_ALLOWED_HOSTS` se leen de variables de entorno. Con `DEBUG=False` es obligatorio definir la clave. |
| `DEBUG` y hosts | `ALLOWED_HOSTS` limitado a `localhost` y `127.0.0.1` por defecto. |
| CSRF | `CsrfViewMiddleware` y `{% csrf_token %}` en todos los formularios POST (incluido el cierre de sesión). |
| XSS | Escapado automático de templates y política CSP (`SECURE_CSP`) que sólo permite recursos del propio sitio. |
| Clickjacking | `X_FRAME_OPTIONS = 'DENY'` y `frame-ancestors 'none'`. |
| Cookies | `HttpOnly` y `SameSite=Lax` para sesión y CSRF; sesión de 1 hora que expira al cerrar el navegador. |
| HTTPS | Con `DEBUG=False`: redirección a HTTPS, cookies `Secure` y HSTS. |
| Contraseñas | Validadores de Django con longitud mínima de 10 caracteres; se almacenan con hash PBKDF2. |
| Inyección SQL | Todas las consultas usan el ORM (consultas parametrizadas). |
| Control de acceso | Vistas protegidas con `login_required` y `permission_required`. |

`python manage.py check --deploy` no informa problemas al ejecutarse con `DJANGO_DEBUG=False` y una `DJANGO_SECRET_KEY` definida.

## Autenticación por roles

La migración `reservas/migrations/0002_roles.py` crea tres grupos con sus permisos:

| Rol | Actividades | Horarios | Inscripciones | Admin |
|---|---|---|---|---|
| Administrador | ver, crear, modificar, eliminar | ver, crear, modificar, eliminar | ver, crear, modificar, eliminar | Sí |
| Coordinador | ver, crear, modificar | ver, crear, modificar | ver, modificar | Sí |
| Socio | ver | ver | – | No |

- Login en `/cuentas/login/` y logout en `/cuentas/logout/`.
- Los usuarios anónimos son redirigidos al login; si el rol no tiene el permiso necesario se muestra la página 403.
- El menú sólo muestra *Agregar actividad* y *Administración* a los roles que pueden usarlos.
- Al asignar o quitar un rol desde el Admin (*Usuarios → Grupos*), `reservas/signals.py` actualiza automáticamente `is_staff`: Administrador y Coordinador acceden al Admin, Socio no.

### Crear usuarios con rol

1. Entrar al Admin como superusuario → *Usuarios* → *Agregar usuario*.
2. En la edición del usuario, elegir el grupo (Administrador, Coordinador o Socio) y guardar.

## Tests

```bash
python manage.py test reservas
```
