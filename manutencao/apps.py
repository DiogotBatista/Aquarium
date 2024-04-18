from django.apps import AppConfig


class ManutencaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manutencao'

    def ready(self):
        # Importa e registra os signals
        import manutencao.signals