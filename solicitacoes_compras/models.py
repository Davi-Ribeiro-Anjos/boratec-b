from django.db import models
from django.utils import timezone

from service.choices import (
    DEPARTAMENTO_CHOICES,
    FORMA_PGT_CHOICES,
    STATUS_CHOICES,
    CATEGORIA_CHOICES,
)


class SolicitacoesCompras(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    numero_solicitacao = models.IntegerField(unique=True)
    data_solicitacao_pra = models.DateField()
    data_solicitacao_bo = models.DateTimeField(default=timezone.now)
    data_vencimento_boleto = models.DateField(null=True, blank=True)
    data_conclusao_pedido = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES.choices)
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
    anexo = models.FileField(upload_to="cpr/%Y/%m/%d", blank=True, null=True)

    filial = models.ForeignKey(
        "filiais.Filiais",
        on_delete=models.PROTECT,
        related_name="solicitacoes_compras",
        null=True,
    )
    solicitante = models.ForeignKey(
        "usuarios.Usuarios",
        on_delete=models.PROTECT,
        related_name="compras_solicitante",
        null=True,
    )
    responsavel = models.ForeignKey(
        "usuarios.Usuarios",
        on_delete=models.PROTECT,
        related_name="compras_responsavel",
        null=True,
    )
    autor = models.ForeignKey(
        "usuarios.Usuarios",
        on_delete=models.PROTECT,
        related_name="compras_autor",
        null=True,
    )
    ultima_atualizacao = models.ForeignKey(
        "usuarios.Usuarios",
        on_delete=models.PROTECT,
        related_name="compras_ultima_att",
        null=True,
    )

    def __repr__(self) -> str:
        return f"<Solicitação Compra {self.numero_solicitacao} - {self.status}>"

    def __str__(self):
        return str(self.placa)

    class Meta:
        verbose_name = "SolicitacaoCompra"
        verbose_name_plural = "SolicitacoesCompras"
        db_table = "solicitacoes_compras"
        app_label = "solicitacoes_compras"
