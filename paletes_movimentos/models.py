from django.db import models
from django.utils import timezone

from filiais.models import Filiais
from funcionarios.models import Funcionarios


class PaletesMovimentos(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    solicitacao = models.CharField(max_length=25)
    data_solicitacao = models.DateTimeField(default=timezone.now)
    data_recebimento = models.DateTimeField(null=True)
    placa_veiculo = models.CharField(max_length=7)
    motorista = models.CharField(max_length=35)
    conferente = models.CharField(max_length=35)
    recebido = models.BooleanField(default=False)
    quantidade_paletes = models.IntegerField()

    origem = models.ForeignKey(
        Filiais, on_delete=models.CASCADE, related_name="paletes_movimentos_origem"
    )
    destino = models.ForeignKey(
        Filiais, on_delete=models.CASCADE, related_name="paletes_movimentos_destino"
    )
    autor = models.ForeignKey(
        Funcionarios, on_delete=models.CASCADE, related_name="paletes_movimentos"
    )

    class Meta:
        verbose_name = "PaleteMovimento"
        verbose_name_plural = "PaletesMovimentos"
        db_table = "paletes_movimentos"
        app_label = "paletes_movimentos"

    def __repr__(self) -> str:
        return f"<Paletes Movimentos {self.pk} - {self.solicitacao}>"

    def __str__(self):
        return f"<Paletes Movimentos {self.pk} - {self.solicitacao}>"
