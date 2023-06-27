from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from funcionarios.models import Funcionarios


class PJEmail(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_envio = models.DateTimeField(default=timezone.now)
    data_pagamento = models.DateField()
    mensagem = models.TextField()

    funcionario = models.ForeignKey(
        Funcionarios, on_delete=models.CASCADE, related_name="emails"
    )
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "PJEmail"
        verbose_name_plural = "PJEmails"
        db_table = "pj_emails"
        app_label = "pj_emails"

    def __repr__(self) -> str:
        return f"<PJ Email {self.id} - {self.funcionario.nome}>"

    def __str__(self):
        return f"<PJ Email {self.id} - {self.funcionario.nome}>"
