from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from filiais.models import Filiais
from pj_complementos.models import PJComplementos


class GENERO_CHOICES(models.TextChoices):
    CISGENERO = "CISGÊNERO"
    TRANSGENERO = "TRANSGÊNERO"
    NAO_BINARIO = "NÃO BINÁRIO"


class EMPRESA_CHOICES(models.TextChoices):
    BORA = "BORA"
    BORBON = "BORBON"
    JC = "JC"
    JSR = "JSR"
    TRANSFOOD = "TRANSFOOD"


class TIPO_CONTRATO_CHOICES(models.TextChoices):
    CLT = "CLT"
    PJ = "PJ"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class Funcionarios(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=40, unique=True)
    genero = models.CharField(max_length=15, choices=GENERO_CHOICES.choices, null=True)
    data_nascimento = models.DateField(null=True)
    rg = models.CharField(max_length=8, validators=[only_int], unique=True, null=True)
    cpf = models.CharField(max_length=11, validators=[only_int], unique=True, null=True)
    cnpj = models.CharField(
        max_length=14, validators=[only_int], unique=True, null=True
    )
    empresa = models.CharField(max_length=15, choices=EMPRESA_CHOICES.choices)
    tipo_contrato = models.CharField(
        max_length=3, choices=TIPO_CONTRATO_CHOICES.choices
    )
    cargo = models.CharField(max_length=40)
    rua = models.CharField(max_length=100, null=True)
    numero = models.CharField(max_length=7, validators=[only_int], null=True)
    complemento = models.CharField(max_length=75, null=True, blank=True)
    cep = models.CharField(max_length=8, validators=[only_int], null=True)
    bairro = models.CharField(max_length=50, null=True)
    cidade = models.CharField(max_length=30, null=True)
    uf = models.CharField(max_length=2, null=True)
    banco = models.CharField(max_length=20, null=True)
    agencia = models.CharField(max_length=5, validators=[only_int], null=True)
    conta = models.CharField(max_length=15, validators=[only_int], null=True)
    operacao = models.IntegerField(null=True)
    pix = models.CharField(max_length=30, null=True)
    data_admissao = models.DateField()
    ativo = models.BooleanField(default=True)

    filial = models.ForeignKey(
        Filiais, on_delete=models.CASCADE, related_name="funcionarios"
    )
    complemento_funcionario = models.OneToOneField(
        PJComplementos,
        on_delete=models.CASCADE,
        related_name="funcionario",
        unique=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="funcionario",
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
        db_table = "funcionarios"
        app_label = "funcionarios"

    def __repr__(self) -> str:
        return f"<Funcionario {self.id} - {self.nome}>"

    def __str__(self):
        return f"<Funcionario {self.id} - {self.nome}>"
