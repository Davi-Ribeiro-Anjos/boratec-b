from django.db import models


class EmployeesDismissals(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    dismissal_date = models.DateField()
    dismissal_motive = models.TextField()

    class Meta:
        verbose_name = "EmployeeDismissal"
        verbose_name_plural = "EmployeesDismissals"
        db_table = "employees_dismissals"
        app_label = "employees_dismissals"

    def __repr__(self) -> str:
        return f"<Employee Dismissal {self.id}>"

    def __str__(self):
        return f"<Employee Dismissal {self.id}>"
