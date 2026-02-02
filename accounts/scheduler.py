from apscheduler.schedulers.background import BackgroundScheduler
from .models import User
from django.utils.timezone import now
from datetime import timedelta



def delete_invalid_users():
    thirty_minutes_ago = now() - timedelta(minutes=5)

    User.objects.filter(
        is_verified = False,
        date_joined__lt=thirty_minutes_ago
    ).delete()
    print("deleted the unverified user.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_invalid_users, 'interval', minutes=5)
    scheduler.start()

