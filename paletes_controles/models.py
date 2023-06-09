from django.db import models
from django.contrib.auth.models import User

from _service.choices import DEPARTAMENTO_CHOICES

from filiais.models import Filiais


class PaletesControles(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    localizacao_atual = models.CharField(max_length=3, null=True, blank=True)
    localizacao_destinatario = models.CharField(max_length=3, null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = "PaleteControle"
        verbose_name_plural = "PaletesControles"
        db_table = "paletes_controles"
        app_label = "paletes_controles"

    def __repr__(self) -> str:
        return f"<Paletes Controles {self.pk} - {self.localizacao_atual}>"

    def __str__(self):
        return f"<Paletes Controles {self.pk} - {self.localizacao_atual}>"
