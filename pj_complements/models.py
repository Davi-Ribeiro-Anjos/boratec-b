from django.db import models


class PJComplements(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    salary = models.FloatField()
    allowance = models.FloatField(default=0)
    college = models.FloatField(default=0)
    housing_allowance = models.FloatField(default=0)
    covenant_credit = models.FloatField(default=0)
    others_credits = models.FloatField(default=0)
    advance_money = models.FloatField(default=0)
    covenant_discount = models.FloatField(default=0)
    others_discounts = models.FloatField(default=0)
    subsistence_allowance = models.FloatField(default=0)
    observation = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "PJComplement"
        verbose_name_plural = "PJComplements"
        db_table = "pj_complements"
        app_label = "pj_complements"

    def __repr__(self) -> str:
        return f"<PJ Complements {self.id}>"

    def __str__(self):
        return f"<PJ Complements {self.id}>"
