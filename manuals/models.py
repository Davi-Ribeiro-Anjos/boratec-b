from django.db import models

from employees.models import Employees


class Manuals(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="manuals/%Y/%m/%d")
    system = models.CharField(max_length=50)
    module = models.CharField(max_length=50)

    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="manuals"
    )

    class Meta:
        verbose_name = "Manual"
        verbose_name_plural = "Manuals"
        db_table = "manuals"
        app_label = "manuals"

    def __repr__(self) -> str:
        return f"<Manual {self.id} - {self.title}>"

    def __str__(self):
        return f"<Manual {self.id} - {self.title}>"
