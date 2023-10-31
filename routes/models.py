from django.db import models

from branches.models import Branches


class TEMPERATURE_CHOICES(models.TextChoices):
    CONGELADO = "CONGELADO"
    REFRIGERADO = "REFRIGERADO"


class COMPANY_CHOICES(models.TextChoices):
    BORA = "BORA"
    BORBON = "BORBON"
    TRANSFOOD = "TRANSFOOD"


class Routes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    uf_name = models.CharField(max_length=4)
    lead_time = models.IntegerField()
    temperature = models.CharField(max_length=11, choices=TEMPERATURE_CHOICES.choices)
    company = models.CharField(max_length=9, choices=COMPANY_CHOICES.choices)
    boarding = models.CharField(max_length=20)
    minimum_weight = models.IntegerField()
    price_per_kilogram_1 = models.FloatField()
    price_per_kilogram_2 = models.FloatField(null=True)
    price_per_kilogram_3 = models.FloatField(null=True)
    delivery_fee = models.FloatField()
    ad_valorem = models.FloatField(default=1)

    origin = models.ForeignKey(
        Branches, on_delete=models.CASCADE, related_name="routes", default=1
    )

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"
        db_table = "routes"
        app_label = "routes"

    def __repr__(self) -> str:
        return f"<Route {self.id} - {self.uf_name}>"

    def __str__(self):
        return f"<Route {self.id} - {self.uf_name}>"
