from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    # enum-класс для пользователя
    ADMIN = 'admin'
    USER = 'user'


class User(AbstractBaseUser):
    # переопределение пользователя
    username = None
    first_name = models.CharField(max_length=40, verbose_name='имя')
    last_name = models.CharField(max_length=40, verbose_name='фамилия')
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = PhoneNumberField(_('Phone'))
    role = models.CharField(max_length=5, choices=UserRoles.choices, default=UserRoles.USER,
                            verbose_name="роль")
    image = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    is_active = models.BooleanField(default=True)

    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'
    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    # для корректной работы также переопределяем менеджер модели пользователя
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
