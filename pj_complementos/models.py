from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PJComplementos(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    salario = models.FloatField()
    ajuda_custo = models.FloatField(default=0)
    faculdade = models.FloatField(default=0)
    credito_convenio = models.FloatField(default=0)
    auxilio_moradia = models.FloatField(default=0)
    outros_creditos = models.FloatField(default=0)
    adiantamento = models.FloatField(default=0)
    desconto_convenio = models.FloatField(default=0)
    outros_descontos = models.FloatField(default=0)
    data_pagamento = models.DateField()
    data_emissao = models.DateTimeField(default=timezone.now)

    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "PJComplemento"
        verbose_name_plural = "PJComplementos"
        db_table = "pj_complementos"
        app_label = "pj_complementos"

    def __repr__(self) -> str:
        return f"<PJ Complementos {self.id}>"

    def __str__(self):
        return f"<PJ Complementos {self.id}>"
