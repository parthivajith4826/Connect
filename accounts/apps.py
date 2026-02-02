from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()

    

    
