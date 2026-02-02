from django.apps import AppConfig


class FreelancerConfig(AppConfig):
    name = "freelancer"

    # To start the scheduler for checking the subscription active or not
    def ready(self):
        from .scheduler import start_subscription_scheduler

        start_subscription_scheduler()
        print("started checking the expired subscription packs")
