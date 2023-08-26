from django.db import models

from employees.models import Employees
from epis_items.models import EPIsItems


class EPIsSizes(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    size = models.CharField(max_length=5, default="UNICO")
    quantity = models.PositiveIntegerField()
    quantity_minimum = models.PositiveIntegerField()
    quantity_provisory = models.PositiveIntegerField()

    item = models.ForeignKey(
        EPIsItems, on_delete=models.CASCADE, related_name="epis_sizes"
    )
    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="epis_sizes"
    )

    class Meta:
        verbose_name = "EPISize"
        verbose_name_plural = "EPIsSizes"
        db_table = "epis_sizes"
        app_label = "epis_sizes"

    def __repr__(self) -> str:
        return f"<EPI Size {self.size} - {self.quantity}>"

    def __str__(self):
        return f"<EPI Size {self.size} - {self.quantity}>"
