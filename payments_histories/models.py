from django.db import models
from django.core.exceptions import ValidationError


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class PaymentsHistories(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=200, null=True, blank=True)
    cnpj = models.CharField(max_length=14, validators=[only_int], null=True)
    bank = models.CharField(max_length=20, null=True)
    agency = models.CharField(max_length=5, validators=[only_int], null=True)
    account = models.CharField(max_length=25, validators=[only_int], null=True)
    operation = models.IntegerField(null=True)
    pix = models.CharField(max_length=30, null=True)

    salary = models.FloatField()
    allowance = models.FloatField(default=0)
    college = models.FloatField(default=0)
    housing_allowance = models.FloatField(default=0)
    covenant_credit = models.FloatField(default=0)
    others_credits = models.FloatField(default=0)
    advance_money = models.FloatField(default=0)
    covenant_discount = models.FloatField(default=0)
    others_discounts = models.FloatField(default=0)
    subsistence_allowance = models.FloatField(default=0)
    observation = models.TextField(blank=True, null=True)

    data_emission = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "PaymentHistory"
        verbose_name_plural = "PaymentsHistories"
        db_table = "payments_histories"
        app_label = "payments_histories"

    def __repr__(self) -> str:
        return f"<Payment History {self.name} - {self.cnpj}>"

    def __str__(self):
        return f"<Payment History {self.name} - {self.cnpj}>"
