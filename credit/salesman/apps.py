from django.apps import AppConfig


class SalesmanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salesman'

    def ready(self):
        from . import signals