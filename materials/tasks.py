from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Subscription, Course


@shared_task
def send_update():
    course = Course.objects.all()
    sub = Subscription.objects.all()
    for user in sub:
        send_mail(
            subject=f'{course.title}',
            message=f'Появилось новое обновление в курсе {course.title}!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[f'{user.user}'],
            fail_silently=True,
        )
