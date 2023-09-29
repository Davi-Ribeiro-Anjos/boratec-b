from django.db import models
from django.core.exceptions import ValidationError


from employees.models import Employees
from vehicles.models import Vehicles


class STATUS_CHOICES(models.TextChoices):
    PARADO = "PARADO"
    PREVENTIVO = "PREVENTIVO"
    FUNCIONANDO = "FUNCIONANDO"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class FleetsAvailabilities(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    date_occurrence = models.DateTimeField(auto_now=True)
    date_forecast = models.DateTimeField(null=True)  # PREVISAO
    date_release = models.DateTimeField(null=True)  # LIBERACAO
    status = models.CharField(max_length=11, choices=STATUS_CHOICES.choices)
    service_order = models.IntegerField(null=True)
    observation = models.TextField(blank=True, null=True)

    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="fleets_availabilities"
    )
    vehicle = models.ForeignKey(
        Vehicles, on_delete=models.CASCADE, related_name="fleets_availabilities"
    )

    class Meta:
        verbose_name = "FleetAvailability"
        verbose_name_plural = "FleetsAvailabilities"
        db_table = "fleets_availabilities"
        app_label = "fleets_availabilities"

    def __repr__(self) -> str:
        return f"<Fleets Availabilities {self.id} - {self.status}>"

    def __str__(self):
        return f"<Fleets Availabilities {self.id} - {self.status}>"
