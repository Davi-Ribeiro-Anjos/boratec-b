from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from employees.models import Employees


class TYPE_PAYMENT_CHOICES(models.TextChoices):
    ADIANTAMENTO = "ADIANTAMENTO"
    PAGAMENTO = "PAGAMENTO"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class PJThirteenths(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    months = models.CharField(max_length=2, validators=[only_int])
    date_payment = models.DateField()
    value = models.FloatField()
    send = models.BooleanField(default=False)
    type_payment = models.CharField(max_length=12, choices=TYPE_PAYMENT_CHOICES.choices)

    employee = models.ForeignKey(
        Employees, on_delete=models.PROTECT, related_name="pj_thirteenths_employees"
    )
    author = models.ForeignKey(
        Employees, on_delete=models.PROTECT, related_name="pj_thirteenths_authors"
    )

    class Meta:
        verbose_name = "PJThirteenth"
        verbose_name_plural = "PJThirteenths"
        db_table = "pj_thirteenths"
        app_label = "pj_thirteenths"

    def __repr__(self) -> str:
        return f"<PJ Thirteenths {self.id} - {self.time}>"

    def __str__(self):
        return f"<PJ Thirteenths {self.id} - {self.time}>"
