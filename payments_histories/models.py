from django.db import models

from employees.models import Employees


class PJMails(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    date_send = models.DateField(auto_now=True)
    date_payment = models.DateField()
    message = models.TextField()

    employee = models.ForeignKey(
        Employees, on_delete=models.CASCADE, related_name="pj_mails"
    )

    class Meta:
        verbose_name = "PJMail"
        verbose_name_plural = "PJsMails"
        db_table = "pj_mails"
        app_label = "pj_mails"

    def __repr__(self) -> str:
        return f"<PJ Mail {self.employee.name}>"

    def __str__(self):
        return f"<PJ Mail {self.employee.name}>"
