from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

"""
Aquí se crea el modelo de un usuario personalizado, se trabaja con este modelo y no
con el modelo de usuario por defecto de django ya que el personalizado es más versátil, 
se pueden agregar atributos, métodos y presenta ventajas en términos de la 
escalabilidad de la app.
"""

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y retorna un usuario con un correo electrónico y contraseña.
        """
        if not email:
            raise ValueError("Se debe proporcionar un correo electrónico")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # Se realiza el hash seguro de la contraseña antes de almacenarla
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y retorna un superusuario con privilegios de administrador.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Se asigna el administrador de objetos personalizado para las acciones del modelo
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        """
        Retorna una cadena que representa al usuario, en este caso con su email.
        """
        return self.email
