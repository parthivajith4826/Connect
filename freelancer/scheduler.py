from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from management.models import UserSubscription


def expire_user_subscriptions():
    """
    Deactivate subscriptions whose end_date has passed
    """
    now = timezone.now()

    expired_count = UserSubscription.objects.filter(
        is_active=True,  # only active subscriptions
        end_date__isnull=False,  # must have an end date
        end_date__lt=now,  # expired
    ).update(is_active=False)

    print(f"{expired_count} subscriptions deactivated")


def start_subscription_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        expire_user_subscriptions,
        trigger="interval",
        minutes=1,
        id="expire_user_subscriptions",
        replace_existing=True,
    )
    scheduler.start()
