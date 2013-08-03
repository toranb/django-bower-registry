from registry.settings.base_settings import *

TEMPLATE_DEBUG = DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '.local_db',
    }
}
