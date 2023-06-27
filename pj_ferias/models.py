from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from funcionarios.models import Funcionarios


class PAGAMENTO_CHOICES(models.TextChoices):
    INTEGRAL = "INTEGRAL"
    PARCIAL = "PARCIAL"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class PJFerias(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    ultimas_ferias_inicio = models.DateField()
    ultimas_ferias_fim = models.DateField()
    periodo = models.CharField(
        max_length=2, validators=[only_int], blank=True, null=True
    )
    quitado = models.BooleanField(default=0)
    vencimento = models.DateField()
    tipo_pagamento = models.CharField(max_length=8, choices=PAGAMENTO_CHOICES.choices)
    agendamento_inicial = models.DateField(blank=True, null=True)
    agendamento_fim = models.DateField(blank=True, null=True)
    valor_integral = models.FloatField(blank=True, null=True)
    valor_parcial_1 = models.FloatField(blank=True, null=True)
    valor_parcial_2 = models.FloatField(blank=True, null=True)
    data_quitacao = models.DateField(blank=True, null=True)
    alerta_venc_enviado = models.BooleanField(default=0)
    observacao = models.TextField(blank=True, null=True)

    funcionario = models.ForeignKey(
        Funcionarios, on_delete=models.CASCADE, related_name="ferias"
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "PJFerias"
        verbose_name_plural = "PJFerias"
        db_table = "pj_ferias"
        app_label = "pj_ferias"

    def __repr__(self) -> str:
        return f"<PJ Ferias {self.id} - {self.funcionario.nome}>"

    def __str__(self):
        return f"<PJ Ferias {self.id} - {self.funcionario.nome}>"
