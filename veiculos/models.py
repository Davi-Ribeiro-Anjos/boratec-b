from django.db import models
from django.core.exceptions import ValidationError

from filiais.models import Filiais


class CODIGO_TIPO_VEICULO_CHOICES(models.TextChoices):
    VAN_PASSAGEIROS = "VAN-PASSAGEIROS"
    CAMINHAO = "CAMINHAO"
    CAVALO = "CAVALO"
    CARRETA = "CARRETA"
    VUC_MINI_CAMINHAO = "VUC-MINI CAMINHAO"
    BI_TRUCK = "BI TRUCK"
    TOCO = "TOCO"
    TRES_POR_QUATRO = "3/4"
    TRUCK = "TRUCK"
    VEICULO_APOIO = "VEICULO APOIO"
    PASSAGEIRO = "PASSAGEIRO"
    PASSAGEIRO_MOVEL = "PASSAGEIRO MOVEL"
    VW_24_280_CRM_6X2 = "VW/24.280 CRM 6X2"
    FIORINO = "FIORINO"
    HR = "HR"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class Veiculos(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    codigo_veiculo = models.CharField(
        max_length=20, choices=CODIGO_TIPO_VEICULO_CHOICES.choices
    )
    placa_veiculo = models.CharField(
        max_length=7,
        unique=True,
    )
    km_atual = models.IntegerField()
    observacao = models.CharField(max_length=30, blank=True, null=True)
    renavam = models.CharField(max_length=11, unique=True, validators=[only_int])
    modelo_veiculo = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)

    filial = models.ForeignKey(
        Filiais, on_delete=models.PROTECT, related_name="veiculos"
    )
    ultimo_dispo_frota = models.ForeignKey(
        "DisponibilidadeFrota", on_delete=models.PROTECT, null=True
    )

    class Meta:
        verbose_name = "Veiculo"
        verbose_name_plural = "Veiculos"
        db_table = "veiculos"
        app_label = "veiculos"

    def __repr__(self) -> str:
        return f"<Veiculo {self.id} - {self.placa_veiculo}>"

    def __str__(self):
        return f"<Veiculo {self.id} - {self.placa_veiculo}>"
