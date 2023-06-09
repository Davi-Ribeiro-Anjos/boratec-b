from django.db import models
from datetime import datetime

from filiais.models import Filiais

# from usuarios.models import Usuarios
from django.contrib.auth.models import User
from _service.choices import (
    DEPARTAMENTO_CHOICES,
    FORMA_PGT_CHOICES,
    STATUS_CHOICES,
    CATEGORIA_CHOICES,
)


class SolicitacoesCompras(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    numero_solicitacao = models.IntegerField(unique=True)
    data_solicitacao_bo = models.DateTimeField(default=datetime.now())
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
        User,
        on_delete=models.PROTECT,
        related_name="compras_solicitante",
        null=True,
    )
    responsavel = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="compras_responsavel",
        null=True,
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="compras_autor",
    )
    ultima_atualizacao = models.ForeignKey(
        User,
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
