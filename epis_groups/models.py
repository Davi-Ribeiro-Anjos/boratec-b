from django.db import models

from employees.models import Employees


class EPIsGroups(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)

    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="epis_groups"
    )

    class Meta:
        verbose_name = "EPIGroup"
        verbose_name_plural = "EPIsGroups"
        db_table = "epis_groups"
        app_label = "epis_groups"

    def __repr__(self) -> str:
        return f"<EPI Group {self.name}>"

    def __str__(self):
        return f"<EPI Group {self.name}>"
