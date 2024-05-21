from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_user_activity():
    users = User.objects.all()
    for user in users:
        if user.last_login and not user.is_active:
            if user.last_login < timezone.now() - timezone.timedelta(days=30):
                user.is_active = False
                user.save()
                print(f"{user.email} заблокирован")
                print(f"{user.email} - активность: {user.is_active} ")
