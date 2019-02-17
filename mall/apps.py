from django.apps import AppConfig

class MallConfig(AppConfig):
    name = 'mall'

    def ready(self):
        from mall import ml_signals

