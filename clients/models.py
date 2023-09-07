from django.db import models
from django.core.exceptions import ValidationError

from branches.models import Branches
from employees.models import Employees


class TYPE_REGISTRATION_CHOICES(models.TextChoices):
    CLIENTE = "CLIENTE"
    MOTORISTA = "MOTORISTA"


class TYPE_PALLET_CHOICES(models.TextChoices):
    PBR = "PBR"
    CHEP = "CHEP"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class Clients(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    document = models.CharField(max_length=14, null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    type_registration = models.CharField(
        max_length=15, choices=TYPE_REGISTRATION_CHOICES.choices
    )
    branches = models.ManyToManyField(
        Branches,
        verbose_name=("clients"),
        through="ClientsBranches",
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        db_table = "clients"
        app_label = "clients"

    def __repr__(self) -> str:
        return f"<Clients {self.pk} - {self.name}>"

    def __str__(self):
        return f"<Clients {self.pk} - {self.name}>"


class ClientsBranches(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    type_pallet = models.CharField(
        max_length=4, choices=TYPE_PALLET_CHOICES.choices, default="PBR", null=True
    )

    class Meta:
        verbose_name = "ClientBranch"
        verbose_name_plural = "ClientsBranches"
        db_table = "clients_branches"

    def __repr__(self) -> str:
        return f"<Clients Branches {self.pk} - {self.balance}>"

    def __str__(self):
        return f"<Clients Branches {self.pk} - {self.balance}>"
