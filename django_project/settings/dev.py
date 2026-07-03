"""
Development settings
"""

import socket  # only if you haven't already imported this

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DATABASE_HOST"),
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PORT": os.environ.get("DATABASE_PORT", 5432),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
    }
}

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

SWAGGER_SETTINGS = {
    "VALIDATOR_URLS": [
        "http://localhost:8000/__debug__/",  # Agregue la ruta a la barra de herramientas de depuración aquí
    ],
}

# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
# INSTALLED_APPS += ["debug_toolbar"]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
