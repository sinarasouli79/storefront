from .common import *

SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'
DEBUG = True

MIDDLEWARE += ['silk.middleware.SilkyMiddleware', ]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront2',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '02020255',
        'OPTIONS': {
            "init_command": "SET GLOBAL max_connections = 100000",
        }
    }
}
