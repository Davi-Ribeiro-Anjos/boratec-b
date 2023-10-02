from django.db import models
from django.utils import timezone

from employees.models import Employees
from purchases_requests.models import PurchasesRequests


class PurchasesEntries(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    observation = models.TextField()
    file_1 = models.FileField(
        upload_to="purchases_entries/%Y/%m/%d", blank=True, null=True
    )
    file_2 = models.FileField(
        upload_to="purchases_entries/%Y/%m/%d", blank=True, null=True
    )
    file_3 = models.FileField(
        upload_to="purchases_entries/%Y/%m/%d", blank=True, null=True
    )
    date_creation = models.DateTimeField(default=timezone.now)

    request = models.ForeignKey(
        PurchasesRequests, on_delete=models.CASCADE, related_name="purchases_entries"
    )
    author = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="purchases_entries"
    )

    class Meta:
        verbose_name = "PurchaseEntry"
        verbose_name_plural = "PurchasesEntries"
        db_table = "purchases_entries"
        app_label = "purchases_entries"

    def __repr__(self) -> str:
        return f"<Purchase Entry {self.id} - {self.request.number_request}>"

    def __str__(self):
        return f"<Purchase Entry {self.id} - {self.request.number_request}>"
