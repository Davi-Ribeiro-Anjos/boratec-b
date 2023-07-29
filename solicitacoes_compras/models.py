from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from filiais.models import Filiais
from funcionarios.models import Funcionarios


class STATUS_CHOICES(models.TextChoices):
    ABERTO = "ABERTO"
    ANDAMENTO = "ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"


class DEPARTAMENTO_CHOICES(models.TextChoices):
    DEFAULT = "NÃO INFORMADO"
    DIRETORIA = "DIRETORIA"
    FATURAMENTO = "FATURAMENTO"
    FINANCEIRO = "FINANCEIRO"
    RH = "RH"
    FISCAL = "FISCAL"
    MONITORAMENTO = "MONITORAMENTO"
    OPERACIONAL = "OPERACIONAL"
    FROTA = "FROTA"
    EXPEDICAO = "EXPEDICAO"
    COMERCIAL = "COMERCIAL"
    JURIDICO = "JURIDICO"
    DESENVOLVIMENTO = "DESENVOLVIMENTO"
    TI = "TI"
    FILIAIS = "FILIAIS"
    COMPRAS = "COMPRAS"


class FORMA_PGT_CHOICES(models.TextChoices):
    DEFAULT = "NÃO INFORMADO"
    A_VISTA = "A VISTA"
    PARCELADO_1X = "PARCELADO 1X"
    PARCELADO_2X = "PARCELADO 2X"
    PARCELADO_3X = "PARCELADO 3X"
    PARCELADO_4X = "PARCELADO 4X"
    PARCELADO_5X = "PARCELADO 5X"
    PARCELADO_6X = "PARCELADO 6X"
    PARCELADO_7X = "PARCELADO 7X"
    PARCELADO_8X = "PARCELADO 8X"
    PARCELADO_9X = "PARCELADO 9X"
    PARCELADO_10X = "PARCELADO 10X"
    PARCELADO_11X = "PARCELADO 11X"
    PARCELADO_12X = "PARCELADO 12X"


class CATEGORIA_CHOICES(models.TextChoices):
    DEFAULT = "NÃO INFORMADO"
    ALMOXARIFADO = "ALMOXARIFADO"
    COTACAO = "COTACAO"
    NOTA_FISCAL = "NOTA FISCAL"


class SolicitacoesCompras(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    numero_solicitacao = models.IntegerField(unique=True)
    data_solicitacao_bo = models.DateTimeField(default=timezone.now)
    data_vencimento_boleto = models.DateField(null=True, blank=True)
    data_conclusao_pedido = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES.choices, default="ABERTO"
    )
    departamento = models.CharField(
        max_length=30,
        default=DEPARTAMENTO_CHOICES.DEFAULT,
        choices=DEPARTAMENTO_CHOICES.choices,
        null=True,
        blank=True,
    )
    categoria = models.CharField(
        max_length=30,
        default=CATEGORIA_CHOICES.DEFAULT,
        choices=CATEGORIA_CHOICES.choices,
        null=True,
        blank=True,
    )
    forma_pagamento = models.CharField(
        max_length=30,
        default=FORMA_PGT_CHOICES.DEFAULT,
        choices=FORMA_PGT_CHOICES.choices,
        null=True,
        blank=True,
    )
    pago = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)
    anexo = models.FileField(upload_to="compras/%Y/%m/%d", blank=True, null=True)

    filial = models.ForeignKey(
        Filiais,
        on_delete=models.PROTECT,
        related_name="solicitacoes_compras",
    )
    solicitante = models.ForeignKey(
        Funcionarios,
        on_delete=models.PROTECT,
        related_name="compras_solicitante",
    )
    responsavel = models.ForeignKey(
        Funcionarios,
        on_delete=models.PROTECT,
        related_name="compras_responsavel",
        null=True,
    )
    autor = models.ForeignKey(
        Funcionarios,
        on_delete=models.CASCADE,
        related_name="compras_autor",
    )
    ultima_atualizacao = models.ForeignKey(
        Funcionarios,
        on_delete=models.CASCADE,
        related_name="compras_ultima_att",
    )

    class Meta:
        verbose_name = "SolicitacaoCompra"
        verbose_name_plural = "SolicitacoesCompras"
        db_table = "solicitacoes_compras"
        app_label = "solicitacoes_compras"

    def __repr__(self) -> str:
        return f"<Solicitação Compra {self.numero_solicitacao} - {self.status}>"

    def __str__(self):
        return f"<Solicitação Compra {self.numero_solicitacao} - {self.status}>"
