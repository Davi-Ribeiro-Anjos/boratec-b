from django.db import models


class FuncionariosEPIs(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    celular_modelo = models.CharField(max_length=50, null=True, unique=True)
    celular_numero_ativo = models.IntegerField(null=True, unique=True)
    notebook_modelo = models.IntegerField(null=True, unique=True)
    notebook_numero_ativo = models.IntegerField(null=True, unique=True)

    class Meta:
        verbose_name = "FuncionarioEPI"
        verbose_name_plural = "FuncionariosEPIs"
        db_table = "funcionarios_epis"
        app_label = "funcionarios_epis"

    def __repr__(self) -> str:
        return f"<Funcionario EPIs {self.id}"

    def __str__(self):
        return f"<Funcionario EPIs {self.id}"
