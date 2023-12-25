from django.apps import AppConfig


class AppnameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.appname'
    # I had to change it from appname to apps.appname!!!
