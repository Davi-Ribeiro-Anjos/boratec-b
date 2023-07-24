from django.db import models

from funcionarios.models import Funcionarios


class TIPO_PALETE_CHOICES(models.TextChoices):
    PBR = "PBR"
    CHEP = "CHEP"


class PaletesControles(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    localizacao_atual = models.CharField(max_length=3)
    destino = models.CharField(max_length=3, null=True, blank=True)
    movimento_atual = models.CharField(max_length=25, null=True, blank=True)
    tipo_palete = models.CharField(
        max_length=4,
        choices=TIPO_PALETE_CHOICES.choices,
    )

    autor = models.ForeignKey(
        Funcionarios, on_delete=models.CASCADE, related_name="paletes_controles"
    )

    class Meta:
        verbose_name = "PaleteControle"
        verbose_name_plural = "PaletesControles"
        db_table = "paletes_controles"
        app_label = "paletes_controles"

    def __repr__(self) -> str:
        return f"<Paletes Controles {self.pk} - {self.localizacao_atual}>"

    def __str__(self):
        return f"<Paletes Controles {self.pk} - {self.localizacao_atual}>"
