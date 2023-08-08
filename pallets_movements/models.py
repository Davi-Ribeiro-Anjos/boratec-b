from django.db import models
from django.utils import timezone

from branches.models import Branches
from employees.models import Employees


class PalletsMovements(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    request = models.CharField(max_length=25)
    date_request = models.DateTimeField(default=timezone.now)
    date_received = models.DateTimeField(null=True)
    vehicle_plate = models.CharField(max_length=7)
    driver = models.CharField(max_length=35)
    checker = models.CharField(max_length=35)
    received = models.BooleanField(default=False)
    quantity_pallets = models.IntegerField()

    origin = models.ForeignKey(
        Branches, on_delete=models.CASCADE, related_name="pallets_movements_origin"
    )
    destiny = models.ForeignKey(
        Branches, on_delete=models.CASCADE, related_name="pallets_movements_destiny"
    )
    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="pallets_movements"
    )

    class Meta:
        verbose_name = "PalletMovement"
        verbose_name_plural = "PalletsMovements"
        db_table = "pallets_movements"
        app_label = "pallets_movements"

    def __repr__(self) -> str:
        return f"<Pallets Movements {self.pk} - {self.request}>"

    def __str__(self):
        return f"<Pallets Movements {self.pk} - {self.request}>"
