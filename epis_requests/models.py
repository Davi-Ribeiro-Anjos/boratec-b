from django.db import models

from branches.models import Branches
from employees.models import Employees


class EPIsRequests(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    date_requested = models.DateField(auto_now_add=True)
    date_send = models.DateField(null=True)
    date_confirmed = models.DateField(null=True)
    date_canceled = models.DateField(null=True)
    attachment_confirm = models.FileField(
        upload_to="epis_requests/%Y/%m/%d", blank=True, null=True
    )

    branch = models.ForeignKey(
        Branches, on_delete=models.CASCADE, related_name="epis_requests"
    )
    employee = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="epis_requests"
    )
    author_create = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="epis_requests_create"
    )
    author_confirm = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name="epis_requests_confirm",
        null=True,
    )
    author_cancel = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name="epis_requests_cancel",
        null=True,
    )

    class Meta:
        verbose_name = "EPIRequest"
        verbose_name_plural = "EPIsRequests"
        db_table = "epis_requests"
        app_label = "epis_requests"

    def __repr__(self) -> str:
        return f"<EPI Request {self.employee.name} - {self.date_requested}>"

    def __str__(self):
        return f"<EPI Request {self.employee.name} - {self.date_requested}>"
