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

Luego abrir <http://127.0.0.1:8000/> en el navegador: se muestra la página de bienvenida de Django.
