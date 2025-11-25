from django.apps import AppConfig

class FinanceiroRhConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financeiro_rh'

    def ready(self):
        import financeiro_rh.signals