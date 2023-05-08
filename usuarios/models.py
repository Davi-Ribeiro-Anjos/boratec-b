from django.contrib.auth.models import AbstractUser


class Usuarios(AbstractUser):
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuarios"
        app_label = "usuarios"

    def __str__(self):
        return str(self.username)
