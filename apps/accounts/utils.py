from datetime import timedelta
from django.utils import timezone
import random
from django.core.mail import send_mail
from core import settings

def generate_verification_code():
    return str(random.randint(100000, 999999))

def can_send_new_code(last_sent_time, cooldown_seconds=120):
    if not last_sent_time:
        return True
    return timezone.now() > last_sent_time + timedelta(seconds=cooldown_seconds)

def send_verification_email(email, verification_code):
    subject = 'Ваш код верификации'
    message = f'Ваш код верификации: {verification_code}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, email_from, recipient_list)

def send_password_reset_email(email, reset_code):
    subject = 'Код для сброса пароля'
    message = f'Ваш код для сброса пароля: {reset_code}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, email_from, recipient_list)
    