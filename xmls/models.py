from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class Xmls(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    date_published = models.DateTimeField(auto_now=True)
    date_emission = models.DateTimeField()
    nf = models.IntegerField()
    sender = models.CharField(max_length=200)  # Remetente
    recipient = models.CharField(max_length=200)
    weight = models.FloatField()
    volume = models.IntegerField()
    value_nf = models.FloatField()
    district = models.CharField(max_length=50)
    cep = models.CharField(max_length=8, validators=[only_int])
    county = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    printed = models.BooleanField(default=False)
    xml_file = models.FileField(upload_to="xmls/%Y/%m/%d")

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="xmls",
        null=True,
    )

    class Meta:
        verbose_name = "Xml"
        verbose_name_plural = "Xmls"
        db_table = "xmls"
        app_label = "xmls"

    def __repr__(self) -> str:
        return f"<Xml {self.id} - {self.nf}>"

    def __str__(self):
        return f"<Xml {self.id} - {self.nf}>"
