from django.db import models
from django.contrib.auth.models import User
from datetime import date

from solicitacoes_compras.models import SolicitacoesCompras


class SolicitacoesEntradas(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    observacao = models.TextField()
    arquivo_1 = models.FileField(upload_to="compras/%Y/%m/%d", blank=True, null=True)
    arquivo_2 = models.FileField(upload_to="compras/%Y/%m/%d", blank=True, null=True)
    arquivo_3 = models.FileField(upload_to="compras/%Y/%m/%d", blank=True, null=True)
    data_criacao = models.DateField(default=date.today())
    solicitacao = models.ForeignKey(SolicitacoesCompras, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

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
