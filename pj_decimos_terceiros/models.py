from django.db import models
from django.contrib.auth.models import User

from funcionarios.models import Funcionarios


class PJDecimosTerceiros(models.Model):
    id = models.BigAutoField(primary_key=True)
    valor = models.FloatField()
    periodo_meses = models.IntegerField()
    parcela_1 = models.DateField()
    parcela_2 = models.DateField(blank=True, null=True)

    funcionario = models.ForeignKey(
        Funcionarios,
        on_delete=models.PROTECT,
        related_name="decimos_terceiros_funcionario",
    )
    autor = models.ForeignKey(
        Funcionarios, on_delete=models.PROTECT, related_name="decimos_terceiros_autor"
    )

    class Meta:
        verbose_name = "PJDecimoTerceiro"
        verbose_name_plural = "PJDecimosTerceiros"
        db_table = "pj_decimos_terceiros"
        app_label = "pj_decimos_terceiros"

    def __repr__(self) -> str:
        return f"<PJ Decimo Terceiro {self.id} - {self.funcionario.nome}>"

    def __str__(self):
        return f"<PJ Decimo Terceiro {self.id} - {self.funcionario.nome}>"
