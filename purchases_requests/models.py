from django.db import models
from django.utils import timezone

from branches.models import Branches
from employees.models import Employees


class STATUS_CHOICES(models.TextChoices):
    ABERTO = "ABERTO"
    ANDAMENTO = "ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"


class DEPARTMENT_CHOICES(models.TextChoices):
    DEFAULT = "NAO INFORMADO"
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


class PAYMENT_METHOD_CHOICES(models.TextChoices):
    DEFAULT = "NAO INFORMADO"
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


class CATEGORY_CHOICES(models.TextChoices):
    DEFAULT = "NAO INFORMADO"
    ALMOXARIFADO = "ALMOXARIFADO"
    COTACAO = "COTACAO"
    NOTA_FISCAL = "NOTA FISCAL"


class PurchasesRequests(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    number_request = models.IntegerField(unique=True)
    date_request = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateField(null=True, blank=True)
    date_completion = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES.choices, default="ABERTO"
    )
    department = models.CharField(
        max_length=30,
        default=DEPARTMENT_CHOICES.DEFAULT,
        choices=DEPARTMENT_CHOICES.choices,
        null=True,
        blank=True,
    )
    category = models.CharField(
        max_length=30,
        default=CATEGORY_CHOICES.DEFAULT,
        choices=CATEGORY_CHOICES.choices,
        null=True,
        blank=True,
    )
    payment_method = models.CharField(
        max_length=30,
        default=PAYMENT_METHOD_CHOICES.DEFAULT,
        choices=PAYMENT_METHOD_CHOICES.choices,
        null=True,
        blank=True,
    )
    paid = models.BooleanField(default=False)
    observation = models.TextField(null=True, blank=True)
    attachment = models.FileField(
        upload_to="purchases_requests/%Y/%m/%d", blank=True, null=True
    )

    branch = models.ForeignKey(
        Branches,
        on_delete=models.PROTECT,
        related_name="purchases_requests",
    )
    requester = models.ForeignKey(
        Employees,
        on_delete=models.PROTECT,
        related_name="purchase_requester",
    )
    responsible = models.ForeignKey(
        Employees,
        on_delete=models.PROTECT,
        related_name="purchase_responsible",
        null=True,
    )
    author = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name="purchase_author",
    )
    latest_updater = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name="purchase_latest_updater",
    )

    class Meta:
        verbose_name = "PurchaseRequest"
        verbose_name_plural = "PurchasesRequests"
        db_table = "purchases_requests"
        app_label = "purchases_requests"

    def __repr__(self) -> str:
        return f"<Purchase Request {self.number_request} - {self.status}>"

    def __str__(self):
        return f"<Purchase Request {self.number_request} - {self.status}>"
