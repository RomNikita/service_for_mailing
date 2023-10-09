from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class User(AbstractUser, PermissionsMixin):
    username = None

    email = models.EmailField(max_length=150, verbose_name='электронная почта', unique=True)
    password = models.CharField(max_length=100, verbose_name='пароль')
    phone = models.CharField(max_length=50, unique=True, verbose_name='номер телефона', null=True, blank=True)
    avatar = models.ImageField(upload_to='user', null=True, blank=True, verbose_name='аватар')
    country = models.CharField(max_length=40, null=True, blank=True, verbose_name='страна')
    verification_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='код подтверждения')
    is_active = models.BooleanField(default=False, verbose_name='признак верификации')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CustomPermissionsForUser(models.Model):
    class Meta:
        permissions = [
            ("can_block_users", "Can block users")
        ]
