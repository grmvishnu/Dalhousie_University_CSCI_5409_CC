from .common import *  # NOQA

DEBUG = True

SECRET_KEY = (
    'django-insecure-x@rgo8^jy#fy@kc+j+r%lhsu_0=+u=m4b8&6uo*=5+2#$^-cjp'
)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}
