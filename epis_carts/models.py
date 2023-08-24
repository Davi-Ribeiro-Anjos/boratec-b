from django.db import models

from employees.models import Employees
from epis_requests.models import EPIsRequests
from epis_sizes.models import EPIsSizes


class EPIsCarts(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    quantity = models.PositiveIntegerField()

    size = models.ForeignKey(
        EPIsSizes, on_delete=models.CASCADE, related_name="epis_carts"
    )
    request = models.ForeignKey(
        EPIsRequests, on_delete=models.CASCADE, related_name="epis_sizes"
    )
    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="epis_sizes"
    )

    class Meta:
        verbose_name = "EPICart"
        verbose_name_plural = "EPIsCarts"
        db_table = "epis_carts"
        app_label = "epis_carts"

    def __repr__(self) -> str:
        return f"<EPI Cart {self.size.size} - {self.quantity}>"

    def __str__(self):
        return f"<EPI Cart {self.size.size} - {self.quantity}>"
