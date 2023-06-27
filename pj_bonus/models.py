from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from funcionarios.models import Funcionarios


class PJBonus(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    valor_pagamento = models.IntegerField()
    data_pagamento = models.DateField()
    observacao = models.TextField()
    quitado = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_quitacao = models.DateField(null=True)

    funcionario = models.ForeignKey(Funcionarios, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)
