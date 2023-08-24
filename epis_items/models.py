from django.db import models

from employees.models import Employees
from epis_groups.models import EPIsGroups


class EPIsItems(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    description = models.CharField(max_length=5, default="UNICO")
    validity = models.DateField()
    ca = models.CharField(max_length=50, null=True)

    group = models.ForeignKey(
        EPIsGroups, on_delete=models.CASCADE, related_name="epis_items"
    )
    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="epis_items"
    )

    class Meta:
        verbose_name = "EPIItem"
        verbose_name_plural = "EPIsItems"
        db_table = "epis_items"
        app_label = "epis_items"

    def __repr__(self) -> str:
        return f"<EPI Item {self.description}>"

    def __str__(self):
        return f"<EPI Item {self.description}>"
