from django.apps import AppConfig


class PuntiInteresseConfig(AppConfig):
    name = 'punti_interesse'

    def ready(self):
        #pylint: disable=unused-import
        import punti_interesse.signals.cas_handlers
