import os.path

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), "sqlite3.db")
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = 'localhost'

DEBUG = True

INSTALLED_APPS = (
    'sampleapp',
    'django.contrib.auth',
    'django.contrib.contenttypes',
)

ROOT_URLCONF = 'sampleproject.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), "templates"),)
