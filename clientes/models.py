from django.db import models
from django.core.exceptions import ValidationError

from filiais.models import Filiais
from funcionarios.models import Funcionarios


class TIPO_CADASTRO_CHOICES(models.TextChoices):
    CLIENTE = "CLIENTE"
    MOTORISTA = "MOTORISTA"


class TIPO_PALETE_CHOICES(models.TextChoices):
    PBR = "PBR"
    CHEP = "CHEP"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class Clientes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    razao_social_motorista = models.CharField(max_length=100, unique=True)
    cnpj_cpf = models.CharField(max_length=14, unique=True)
    observacao = models.TextField(null=True, blank=True)
    tipo_cadastro = models.CharField(
        max_length=15, choices=TIPO_CADASTRO_CHOICES.choices
    )
    autor = models.ForeignKey(
        Funcionarios, on_delete=models.CASCADE, related_name="clientes"
    )
    filiais = models.ManyToManyField(
        Filiais,
        verbose_name=("clientes"),
        through="ClientesFiliais",
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = "clientes"
        app_label = "clientes"

    def __repr__(self) -> str:
        return f"<Clientes {self.pk} - {self.razao_social_motorista}>"

    def __str__(self):
        return f"<Clientes {self.pk} - {self.razao_social_motorista}>"


class ClientesFiliais(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    filial = models.ForeignKey(Filiais, on_delete=models.CASCADE)
    saldo = models.IntegerField(default=0)
    tipo_palete = models.CharField(
        max_length=4, choices=TIPO_PALETE_CHOICES.choices, default="PBR"
    )

    class Meta:
        verbose_name = "ClienteFilial"
        verbose_name_plural = "ClientesFiliais"
        db_table = "clientesfiliais"

    def __repr__(self) -> str:
        return f"<Clientes Filiais {self.pk} - {self.saldo}>"

    def __str__(self):
        return f"<Clientes Filiais {self.pk} - {self.saldo}>"
