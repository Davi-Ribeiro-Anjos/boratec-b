from django.db import models
from django.core.exceptions import ValidationError

from branches.models import Branches
from employees.models import Employees
from roles.models import Roles


class PRIORITY_CHOICES(models.TextChoices):
    NORMAL = "NORMAL"
    MEDIA = "MÉDIA"
    ALTA = "ALTA"


class MOTIVE_CHOICES(models.TextChoices):
    DEMANDA_FIM_DE_ANO = "DEMANDA FIM DE ANO"
    NAO_PERFORMACE = "NÃO PERFORMACE"


class RECRUITER_CHOICES(models.TextChoices):
    LARYSSA_RODRIGUES = "LARYSSA RODRIGUES"
    MELISSA_COSTA = "MELISSA COSTA"
    PAULA_SANTOS = "PAULA SANTOS"
    RAQUEL_SILVA = "RAQUEL SILVA"
    THAYS_ANDRADE = "THAYS ANDRADE"


class STATUS_EMAIL_CHOICES(models.TextChoices):
    NAO_RESPONDIDO = "NÃO RESPONDIDO"
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"


class STATUS_CHOICES(models.TextChoices):
    NOVO = "NOVO"
    EM_ANDAMENTO = "EM ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"


class CONTRACT_MODE_CHOICES(models.TextChoices):
    JA = "JOVEM APRENDIZ"
    CLT = "CLT"
    PJ = "PESSOA JURÍDICA"
    PCD = "PCD"


class DEPARTMENT_CHOICES(models.TextChoices):
    ADMINISTRATIVO = "ADMINISTRATIVO"
    BORRACHARIA = "BORRACHARIA"
    COMPRAS = "COMPRAS"
    DEPARTAMENTO_PESSOAL = "DEPARTAMENTO PESSOAL"
    DESENVOLVIMENTO = "DESENVOLVIMENTO"
    EXPEDICAO = "EXPEDIÇÃO"
    FATURAMENTO = "FATURAMENTO"
    FINANCEIRO = "FINANCEIRO"
    FISCAL = "FISCAL"
    FROTAS = "FROTAS"
    JOVEM_APRENDIZ = "JOVEM APRENDIZ"
    LIMPEZA = "LIMPEZA"
    MANUTENCAO = "MANUTENÇÃO"
    MONITORAMENTO = "MONITORAMENTO"
    OPERACAO = "OPERAÇÃO"
    PORTARIA = "PORTARIA"
    RECURSOS_HUMANOS = "RECURSOS HUMANOS"
    RESERVA = "RESERVA"
    TI = "TI"


class TYPE_VACANCY_CHOICES(models.TextChoices):
    AUMENTO_QUADRO = "AUMENTO DE QUADRO"
    SUBSTITUICAO = "SUBSTITUIÇÃO"
    TERCEIROS = "TERCEIROS"


class COMPANY_CHOICES(models.TextChoices):
    BORA = "BORA"
    JC = "JC"
    JSR = "JSR"


class INITIATIVE_CHOICES(models.TextChoices):
    EMPREGADO = "EMPREGADO"
    EMPREGADOR = "EMPREGADOR"


def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError("Valor digitado não é um número")


class Vacancies(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    replacement = models.CharField(max_length=50, null=True)
    salary_range = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True)
    observation = models.TextField(null=True)
    selected = models.CharField(max_length=255, null=True, blank=True)
    work_schedule = models.TextField(null=True)
    release_status = models.TextField(null=True)
    quantity = models.SmallIntegerField(default=1, null=True)

    date_expected_start = models.DateField()  # DATA PREVISTA DE INICIO
    date_requested = models.DateField(auto_now=True)  # DATA CRIADA
    date_vetta = models.DateField(null=True)  # DATA VETTA
    date_exam = models.DateField(null=True)  # DATA EXAME
    date_closed = models.DateField(null=True)  # DATA FECHAMENTO
    date_limit = models.DateField(null=True)  # DATA LIMITE

    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES.choices)
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.NOVO
    )
    contract_mode = models.CharField(
        max_length=15, choices=CONTRACT_MODE_CHOICES.choices
    )
    department = models.CharField(max_length=21, choices=DEPARTMENT_CHOICES.choices)
    type_vacancy = models.CharField(max_length=17, choices=TYPE_VACANCY_CHOICES.choices)
    company = models.CharField(max_length=4, choices=COMPANY_CHOICES.choices)
    initiative = models.CharField(
        max_length=10, choices=INITIATIVE_CHOICES.choices, null=True
    )
    recruiter = models.CharField(
        max_length=50,
        choices=RECRUITER_CHOICES.choices,
        null=True,
    )
    motive = models.CharField(max_length=25, choices=MOTIVE_CHOICES.choices, null=True)

    approval_manager = models.CharField(
        max_length=14,
        choices=STATUS_EMAIL_CHOICES.choices,
        default=STATUS_EMAIL_CHOICES.NAO_RESPONDIDO,
    )
    comment_manager = models.TextField(null=True, blank=True)
    email_manager = models.CharField(max_length=100, null=True, blank=True)
    email_send_manager = models.BooleanField(default=False)
    approval_regional_manager = models.CharField(
        max_length=14,
        choices=STATUS_EMAIL_CHOICES.choices,
        default=STATUS_EMAIL_CHOICES.NAO_RESPONDIDO,
    )
    comment_regional_manager = models.TextField(null=True, blank=True)
    email_regional_manager = models.CharField(max_length=100, null=True, blank=True)
    email_send_regional_manager = models.BooleanField(default=False)
    approval_rh = models.CharField(
        max_length=14,
        choices=STATUS_EMAIL_CHOICES.choices,
        default=STATUS_EMAIL_CHOICES.NAO_RESPONDIDO,
    )
    comment_rh = models.TextField(null=True, blank=True)
    email_rh = models.CharField(max_length=100, null=True, blank=True)
    email_send_rh = models.BooleanField(default=False)
    approval_director = models.CharField(
        max_length=14,
        choices=STATUS_EMAIL_CHOICES.choices,
        default=STATUS_EMAIL_CHOICES.NAO_RESPONDIDO,
    )
    comment_director = models.TextField(null=True, blank=True)
    email_director = models.CharField(max_length=100, null=True, blank=True)
    email_send_director = models.BooleanField(default=False)

    author = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name="vacancies_author",
    )
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, related_name="vacancies")
    branch = models.ForeignKey(
        Branches,
        on_delete=models.PROTECT,
        related_name="vacancies",
    )

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
        db_table = "vacancies"
        app_label = "vacancies"

    def __repr__(self) -> str:
        return f"<Vacancy {self.id} - {self.title}>"

    def __str__(self):
        return f"<Vacancy {self.id} - {self.title}>"
