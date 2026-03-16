from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email kiritilishi shart')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'owner')  # Superuser avtomatik Owner bo'ladi

        return self.create_user(email, nickname, password, **extra_fields)


class User(AbstractUser):
    # Username maydonini butunlay o'chirib tashlaymiz
    username = None
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)

    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    points = models.IntegerField(default=0)
    last_reply_date = models.DateField(null=True, blank=True)

    objects = UserManager()  # Mana bu joyda yangi managerni ulaymiz

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname