from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

from _service.choices import DEPARTAMENTO_CHOICES

from filiais.models import Filiais


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class ComplementosUsuarios(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    cpf_cnpj = models.CharField(max_length=14, validators=[only_int])
    ramal = models.CharField(max_length=3, validators=[only_int])
    departamento = models.CharField(
        max_length=20,
        choices=DEPARTAMENTO_CHOICES,
        default=DEPARTAMENTO_CHOICES.DEFAULT,
    )
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="complemento"
    )
    filial = models.ForeignKey(Filiais, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "UsuarioComplemento"
        verbose_name_plural = "UsuariosComplementos"
        db_table = "usuarios_complementos"
        app_label = "usuarios_complementeos"

    def __repr__(self) -> str:
        return f"<Usuario Complemento {self.pk} - {self.usuario.username}>"

    def __str__(self):
        return f"<Usuario Complemento {self.pk} - {self.usuario.username}>"
