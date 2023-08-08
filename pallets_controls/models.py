from django.db import models

from employees.models import Employees


class TYPE_PALLET_CHOICES(models.TextChoices):
    PBR = "PBR"
    CHEP = "CHEP"


class PalletsControls(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    current_location = models.CharField(max_length=3)
    destiny = models.CharField(max_length=3, null=True, blank=True)
    current_movement = models.CharField(max_length=25, null=True, blank=True)
    type_pallet = models.CharField(
        max_length=4,
        choices=TYPE_PALLET_CHOICES.choices,
    )

    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="pallets_controls"
    )

    class Meta:
        verbose_name = "PalletControl"
        verbose_name_plural = "PalletsControls"
        db_table = "pallets_controls"
        app_label = "pallets_controls"

    def __repr__(self) -> str:
        return f"<Pallets Controls {self.pk} - {self.current_location}>"

    def __str__(self):
        return f"<Pallets Controls {self.pk} - {self.current_location}>"
