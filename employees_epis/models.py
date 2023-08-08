from django.db import models


class EmployeesEPIs(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    phone_model = models.CharField(
        max_length=50,
        null=True,
    )
    phone_code = models.IntegerField(null=True, unique=True)
    notebook_model = models.CharField(max_length=50, null=True)
    notebook_code = models.IntegerField(null=True, unique=True)

    class Meta:
        verbose_name = "EmployeeEPI"
        verbose_name_plural = "EmployeesEPIs"
        db_table = "employees_epis"
        app_label = "employees_epis"

    def __repr__(self) -> str:
        return f"<Employee EPIs {self.id}"

    def __str__(self):
        return f"<Employee EPIs {self.id}"
