from datetime import timedelta
from django.utils import timezone
import random

def generate_verification_code():
    return str(random.randint(100000, 999999))

def can_send_new_code(user):
    if not user.verification_code_sent_at:
        return True
    return timezone.now() > user.verification_code_sent_at + timedelta(seconds=120)

def send_verification_email(email, verification_code):
    print(f"Email: {email} Verification code: {verification_code}")