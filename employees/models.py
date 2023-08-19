from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from branches.models import Branches
from employees_dismissals.models import EmployeesDismissals
from pj_complements.models import PJComplements
from employees_epis.models import EmployeesEPIs


class GENDER_CHOICES(models.TextChoices):
    HOMEM_CISGENERO = "HOMEM CISGÊNERO"
    HOMEM_TRANSGENERO = "HOMEM TRANSGÊNERO"
    MULHER_CISGENERO = "MULHER CISGÊNERO"
    MULHER_TRANSGENERO = "MULHER TRANSGÊNERO"
    NAO_BINARIO = "NÃO BINÁRIO"
    NAO_QUERO_INFORMAR = "NÃO QUERO INFORMAR"


class COMPANY_CHOICES(models.TextChoices):
    BORA = "BORA"
    BORBON = "BORBON"
    JC = "JC"
    JSR = "JSR"
    TRANSFOOD = "TRANSFOOD"


class TYPE_CONTRACT_CHOICES(models.TextChoices):
    CLT = "CLT"
    PJ = "PJ"


class STATUS_CHOICES(models.TextChoices):
    ATIVO = "ATIVO"
    DEMITIDO = "DEMITIDO"
    AFASTADO = "AFASTADO"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class Employees(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=40)
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES.choices, null=True)
    date_birth = models.DateField(null=True)
    rg = models.CharField(max_length=8, validators=[only_int], null=True)
    cpf = models.CharField(max_length=11, validators=[only_int], null=True)
    cnpj = models.CharField(max_length=14, validators=[only_int], null=True)
    company = models.CharField(max_length=15, choices=COMPANY_CHOICES.choices)
    type_contract = models.CharField(
        max_length=3, choices=TYPE_CONTRACT_CHOICES.choices
    )
    role = models.CharField(max_length=40)
    street = models.CharField(max_length=100, null=True)
    number = models.CharField(max_length=7, validators=[only_int], null=True)
    complement = models.CharField(max_length=75, null=True, blank=True)
    cep = models.CharField(max_length=8, validators=[only_int], null=True)
    district = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=30, null=True)
    uf = models.CharField(max_length=2, null=True)
    bank = models.CharField(max_length=20, null=True)
    agency = models.CharField(max_length=5, validators=[only_int], null=True)
    account = models.CharField(max_length=25, validators=[only_int], null=True)
    operation = models.IntegerField(null=True)
    pix = models.CharField(max_length=30, null=True)
    date_admission = models.DateField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES.choices, default="ATIVO"
    )
    first_access = models.BooleanField(default=True)

    branch = models.ForeignKey(
        Branches, on_delete=models.CASCADE, related_name="employees"
    )
    epi = models.OneToOneField(
        EmployeesEPIs,
        on_delete=models.CASCADE,
        related_name="employee",
        null=True,
        unique=True,
    )
    pj_complements = models.OneToOneField(
        PJComplements,
        on_delete=models.CASCADE,
        related_name="employee",
        null=True,
        unique=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee",
        null=True,
        unique=True,
    )
    dismissal = models.ForeignKey(
        EmployeesDismissals,
        on_delete=models.CASCADE,
        related_name="employee",
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        db_table = "employees"
        app_label = "employees"

    def __repr__(self) -> str:
        return f"<Employee {self.id} - {self.nome}>"

    def __str__(self):
        return f"<Employee {self.id} - {self.nome}>"
