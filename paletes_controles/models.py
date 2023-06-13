from django.db import models
from django.contrib.auth.models import User


class TIPO_PALETE_CHOICES(models.TextChoices):
    PBR = "PBR"
    CHEP = "CHEP"


class PaletesControles(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    localizacao_atual = models.CharField(max_length=3)
    movimento_atual = models.CharField(max_length=25, null=True, blank=True)
    tipo_palete = models.CharField(
        max_length=4,
        choices=TIPO_PALETE_CHOICES.choices,
    )
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "PaleteControle"
        verbose_name_plural = "PaletesControles"
        db_table = "paletes_controles"
        app_label = "paletes_controles"

    def __repr__(self) -> str:
        return f"<Paletes Controles {self.pk} - {self.localizacao_atual}>"

    def __str__(self):
        return f"<Paletes Controles {self.pk} - {self.localizacao_atual}>"
