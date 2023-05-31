from django.db import models


class Usuarios(models.Model):
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuarios"
        app_label = "usuarios"

    def __repr__(self) -> str:
        return f"<Usuario {self.pk} - {self.username}>"

    def __str__(self):
        return f"<Usuario {self.pk} - {self.username}>"
