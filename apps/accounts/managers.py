from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.common.managers import GetOrNoneManager


class CustomUserManager(BaseUserManager, GetOrNoneManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("You must provide a valid email address")

    def validate_user(self, email, password): 
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("Base User Account: An email address is required")

        if not password:
            raise ValueError("User must have a password")

    def create_user(self, email, password, **extra_fields):
        self.validate_user(email, password)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)
