from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from django.contrib.auth.models import User


@shared_task
def subscription_renewal(to_email, subject, message):
    """Информирование об обновлении курса."""
    send_mail(subject, message, settings.EMAIL_HOST_USER[to_email])


@shared_task
def deactivate_inactive_users():
    """
    blocking a user who has not logged in for more than a month
    блокировка пользователя, который не заходил в систему более месяца
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
