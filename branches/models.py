from django.db import models


class Branches(models.Model):
    id = models.IntegerField(primary_key=True)
    id_company = models.IntegerField()
    id_branch = models.IntegerField()
    id_garage = models.IntegerField(unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    cnpj = models.CharField(max_length=14, unique=True)
    company = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        db_table = "branches"
        app_label = "branches"

    def __repr__(self) -> str:
        return f"<Branch {self.id} - {self.abbreviation}>"

    def __str__(self):
        return f"<Branch {self.id} - {self.abbreviation}>"
