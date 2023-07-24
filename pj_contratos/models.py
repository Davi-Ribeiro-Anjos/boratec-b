from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from funcionarios.models import Funcionarios


class PJContratos(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    inicio_contrato = models.DateField()
    final_contrato = models.DateField()
    data_reajuste = models.DateField()
    valor_reajuste = models.IntegerField(null=True)
    anexo = models.FileField(upload_to="contratos/%Y/%m/%d", null=True)
    observacao = models.TextField(null=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(
        Funcionarios, on_delete=models.CASCADE, unique=True, related_name="pj_contratos"
    )

    class Meta:
        verbose_name = "PJContrato"
        verbose_name_plural = "PJContratos"
        db_table = "pj_contratos"
        app_label = "pj_contratos"

    def __repr__(self) -> str:
        return f"<PJ Contratos {self.id}>"

    def __str__(self):
        return f"<PJ Contratos {self.id}>"
