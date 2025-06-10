from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,  PermissionsMixin


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(
        max_length=50, blank=True, verbose_name=(u'Nombres'))
    last_name = models.CharField(
        max_length=50, blank=True, verbose_name=(u'Apellidos'))
    username = models.CharField(
        max_length=50, blank=True, verbose_name=(u'Usuario'))
    email = models.EmailField(
        max_length=100, unique=True, verbose_name=(u'Correo'))
    phone_number = models.CharField(
        max_length=50, blank=True, verbose_name=(u'Teléfono'))

    # required
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name=(u'Creado'))
    last_login = models.DateTimeField(
        auto_now_add=True, verbose_name=(u'Modificado'))
    is_admin = models.BooleanField(
        default=False, verbose_name=(u'Administrador'))
    is_staff = models.BooleanField(default=False, verbose_name=(u'Grupo'))
    is_active = models.BooleanField(default=True, verbose_name=(u'Activo'))
    is_superadmin = models.BooleanField(
        default=False, verbose_name=(u'SuperAdmin'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


