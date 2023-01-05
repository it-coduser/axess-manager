from django.apps import AppConfig


class DefaultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'app.rest'
    verbose_name = 'REST API'
