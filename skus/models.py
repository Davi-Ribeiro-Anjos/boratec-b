from django.db import models

from xmls.models import Xmls


class Skus(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    code = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    type_unity = models.CharField(max_length=10)
    quantity_unity = models.IntegerField()
    type_volume = models.CharField(max_length=10)
    quantity_volume = models.IntegerField()

    xml = models.ForeignKey(Xmls, related_name="skus", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Sku"
        verbose_name_plural = "Skus"
        db_table = "skus"
        app_label = "skus"

    def __repr__(self) -> str:
        return f"<Sku {self.id} - {self.code}>"

    def __str__(self):
        return f"<Sku {self.id} - {self.code}>"
