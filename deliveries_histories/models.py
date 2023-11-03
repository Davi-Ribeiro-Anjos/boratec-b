from django.db import models
from django.core.exceptions import ValidationError
from branches.models import Branches

from employees.models import Employees


class DOCUMENT_TYPE_CHOICES(models.TextChoices):
    NFS = "NFS"
    CTE = "CTE"


class DESCRIPTION_JUSTIFICATION_CHOICES(models.TextChoices):
    FERIADO_NACIONAL = "FERIADO NACIONAL"
    FERIADOS_MUNICIPAIS_ESTADUAIS = "FERIADOS MUNICIPAIS / ESTADUAIS"
    ENTREGA_AGENDADA = "ENTREGA AGENDADA"
    CLIENTE_COM_RETENÇÃO_FISCAL = "CLIENTE COM RETENÇÃO FISCAL"
    DESTINATARIO_NÃO_RECEBEU_O_XML = "DESTINATARIO NÃO RECEBEU O XML"
    NF_SEM_PEDIDO = "NF SEM PEDIDO"
    PEDIDO_EXPIRADO = "PEDIDO EXPIRADO"
    EXCESSO_DE_VEICULOS = "EXCESSO DE VEICULOS"
    GRADE_FIXA = "GRADE FIXA"
    DEVOLUÇÃO_TOTAL = "DEVOLUÇÃO TOTAL "
    ATRASO_NA_TRANSFERENCIA = "ATRASO NA TRANSFERENCIA"
    CUSTO = "CUSTO"
    ENTREGUE_SEM_LEAD_TIME = "ENTREGUE SEM LEAD TIME"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class DeliveriesHistories(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    garage = models.CharField(max_length=5)
    id_garage = models.CharField(max_length=5)
    cte = models.CharField(max_length=15, validators=[only_int])
    date_emission = models.DateField()
    lead_time = models.DateField()  # Data Previsao / Lead Time
    date_delivery = models.DateField()  # Data Entrega
    recipient = models.CharField(max_length=200)  # Destinatario
    sender = models.CharField(max_length=200)  # Remetente
    delivery_location = models.CharField(max_length=100)
    weight = models.FloatField(default=0)
    opened = models.SmallIntegerField(default=0)
    nf = models.TextField()
    document_type = models.CharField(
        max_length=3, choices=DOCUMENT_TYPE_CHOICES.choices
    )
    description_justification = models.CharField(
        max_length=50, choices=DESCRIPTION_JUSTIFICATION_CHOICES.choices, null=True
    )
    file = models.FileField(upload_to="justification/%Y/%m/%d", null=True)
    confirmed = models.BooleanField(default=False)
    refuse = models.BooleanField(default=False)

    author_responsible = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name="deliveries_histories_responsible",
        null=True,
    )
    author = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name="deliveries_histories",
        null=True,
    )
    branch = models.ForeignKey(
        Branches,
        on_delete=models.CASCADE,
        related_name="deliveries_histories",
        default=999,
    )

    class Meta:
        verbose_name = "DeliveryHistory"
        verbose_name_plural = "DeliveriesHistories"
        db_table = "deliveries_histories"
        app_label = "deliveries_histories"

    def __repr__(self) -> str:
        return f"<Delivery History {self.id} - {self.cte}>"

    def __str__(self):
        return f"<Delivery History {self.id} - {self.cte}>"
