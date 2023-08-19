from django.db import models
from django.core.exceptions import ValidationError
from branches.models import Branches


class TYPE_VEHICLE_CHOICES(models.TextChoices):
    VAN_PASSAGEIROS = "VAN-PASSAGEIROS"
    CAMINHAO = "CAMINHAO"
    CAVALO = "CAVALO"
    CARRETA = "CARRETA"
    VUC_MINI_CAMINHAO = "VUC-MINI CAMINHAO"
    BI_TRUCK = "BI TRUCK"
    TOCO = "TOCO"
    TRES_QUARTOS = "3/4"
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


class Vehicles(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    type_vehicle = models.CharField(
        max_length=20,
        choices=TYPE_VEHICLE_CHOICES.choices,
        null=True,  # APÓS TESTE TIRAR NULL
    )
    vehicle_plate = models.CharField(max_length=7, unique=True)
    vehicle_mileage = models.IntegerField()
    renavam = models.CharField(max_length=11, validators=[only_int])
    model_vehicle = models.CharField(max_length=20)
    observation = models.CharField(max_length=50, blank=True, null=True)
    last_movement = models.IntegerField(null=True)
    active = models.BooleanField(default=True)

    branch = models.ForeignKey(
        Branches,
        on_delete=models.CASCADE,
        related_name="vehicles",
        default=99,
    )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        db_table = "vehicles"
        app_label = "vehicles"

    def __repr__(self) -> str:
        return f"<Vehicle {self.id} - {self.vehicle_plate}>"

    def __str__(self):
        return f"<Vehicle {self.id} - {self.vehicle_plate}>"
