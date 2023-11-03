from django.db import models

from branches.models import Branches
from routes.models import Routes


class TEMPERATURE_CHOICES(models.TextChoices):
    CONGELADO = "CONGELADO"
    REFRIGERADO = "REFRIGERADO"


class COMPANY_CHOICES(models.TextChoices):
    BORA = "BORA"
    BORBON = "BORBON"
    TRANSFOOD = "TRANSFOOD"


class RoutesLeadTimes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    municipality = models.CharField(max_length=50)
    company = models.CharField(max_length=9, choices=COMPANY_CHOICES.choices)

    branch = models.ForeignKey(
        Branches, on_delete=models.CASCADE, related_name="routes_lead_times"
    )
    route = models.ForeignKey(
        Routes, on_delete=models.CASCADE, related_name="routes_lead_times"
    )

    class Meta:
        verbose_name = "RouteLeadTime"
        verbose_name_plural = "RoutesLeadTimes"
        db_table = "routes_lead_times"
        app_label = "routes_lead_times"

    def __repr__(self) -> str:
        return f"<Route Lead Time {self.id} - {self.municipality}>"

    def __str__(self):
        return f"<Route Lead Time {self.id} - {self.municipality}>"
