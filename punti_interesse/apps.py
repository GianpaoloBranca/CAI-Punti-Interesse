from django.apps import AppConfig


class PuntiInteresseConfig(AppConfig):
    name = 'punti_interesse'

    def ready(self):
        import punti_interesse.signals.cas_handlers
