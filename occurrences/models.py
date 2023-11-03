from django.db import models

from deliveries_histories.models import DeliveriesHistories
from branches.models import Branches


class DOCUMENT_TYPE_CHOICES(models.TextChoices):
    NFS = "NFS"
    CTE = "CTE"


class Occurrences(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    date_emission = models.DateField()
    document_type = models.CharField(
        max_length=3, choices=DOCUMENT_TYPE_CHOICES.choices
    )
    occurrence_code = models.CharField(max_length=5)
    occurrence_description = models.CharField(max_length=200)

    branch = models.ForeignKey(
        Branches,
        on_delete=models.CASCADE,
        related_name="occurrences",
        default=999,
    )

    justification = models.ForeignKey(
        DeliveriesHistories,
        related_name="occurrences",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Occurrence"
        verbose_name_plural = "Occurrences"
        db_table = "occurrences"
        app_label = "occurrences"

    def __repr__(self) -> str:
        return f"<Occurrence {self.id} - {self.cte}>"

    def __str__(self):
        return f"<Occurrence {self.id} - {self.cte}>"
