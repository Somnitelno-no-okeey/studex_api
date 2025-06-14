from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.accounts.managers import CustomUserManager
from apps.common.models import IsDeletedModel
from apps.accounts.utils import can_send_new_code

class User(AbstractBaseUser, PermissionsMixin, IsDeletedModel):
    first_name = models.CharField(verbose_name="Имя", max_length=150, null=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=150, null=True)
    patronymic = models.CharField(verbose_name="Отчество", max_length=150, null=True)
    email = models.EmailField(verbose_name="Email адрес", blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verificated = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_sent_at = models.DateTimeField(null=True, blank=True)
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)
    password_reset_code_sent_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def can_send_new_verification_code(self):
        return can_send_new_code(self.verification_code_sent_at)
    
    def can_send_new_password_reset_code(self):
        return can_send_new_code(self.password_reset_code_sent_at)
    
    def get_full_name(self):
        return " ".join(filter(None, [self.last_name, self.first_name, self.patronymic]))

    def __str__(self):
        return self.get_full_name() or self.email