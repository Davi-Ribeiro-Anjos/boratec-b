from django.db import models
from django.utils import timezone

from funcionarios.models import Funcionarios
from solicitacoes_compras.models import SolicitacoesCompras


class SolicitacoesEntradas(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    observacao = models.TextField()
    arquivo_1 = models.FileField(upload_to="compras/%Y/%m/%d", blank=True, null=True)
    arquivo_2 = models.FileField(upload_to="compras/%Y/%m/%d", blank=True, null=True)
    arquivo_3 = models.FileField(upload_to="compras/%Y/%m/%d", blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    solicitacao = models.ForeignKey(SolicitacoesCompras, on_delete=models.CASCADE)
    autor = models.ForeignKey(
        Funcionarios, on_delete=models.CASCADE, related_name="solicitacoes_entradas"
    )

    class Meta:
        verbose_name = "SolicitacaoEntrada"
        verbose_name_plural = "SolicitacoesEntradas"
        db_table = "solicitacoes_entradas"
        app_label = "solicitacoes_entradas"

    def __repr__(self) -> str:
        return (
            f"<Solicitação Entrada {self.id} - {self.solicitacao.numero_solicitacao}>"
        )

    def __str__(self):
        return (
            f"<Solicitação Entrada {self.id} - {self.solicitacao.numero_solicitacao}>"
        )
