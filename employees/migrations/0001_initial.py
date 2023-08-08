# Generated by Django 3.2.19 on 2023-08-08 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import employees.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branches', '0001_initial'),
        ('employees_epis', '0001_initial'),
        ('pj_complements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('gender', models.CharField(choices=[('HOMEM CISGÊNERO', 'Homem Cisgenero'), ('HOMEM TRANSGÊNERO', 'Homem Transgenero'), ('MULHER CISGÊNERO', 'Mulher Cisgenero'), ('MULHER TRANSGÊNERO', 'Mulher Transgenero'), ('NÃO BINÁRIO', 'Nao Binario'), ('NÃO QUERO INFORMAR', 'Nao Quero Informar')], max_length=25, null=True)),
                ('date_birth', models.DateField(null=True)),
                ('rg', models.CharField(max_length=8, null=True, unique=True, validators=[employees.models.only_int])),
                ('cpf', models.CharField(max_length=11, null=True, unique=True, validators=[employees.models.only_int])),
                ('cnpj', models.CharField(max_length=14, null=True, unique=True, validators=[employees.models.only_int])),
                ('company', models.CharField(choices=[('BORA', 'Bora'), ('BORBON', 'Borbon'), ('JC', 'Jc'), ('JSR', 'Jsr'), ('TRANSFOOD', 'Transfood')], max_length=15)),
                ('type_contract', models.CharField(choices=[('CLT', 'Clt'), ('PJ', 'Pj')], max_length=3)),
                ('role', models.CharField(max_length=40)),
                ('street', models.CharField(max_length=100, null=True)),
                ('number', models.CharField(max_length=7, null=True, validators=[employees.models.only_int])),
                ('complement', models.CharField(blank=True, max_length=75, null=True)),
                ('cep', models.CharField(max_length=8, null=True, validators=[employees.models.only_int])),
                ('district', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=30, null=True)),
                ('uf', models.CharField(max_length=2, null=True)),
                ('bank', models.CharField(max_length=20, null=True)),
                ('agency', models.CharField(max_length=5, null=True, validators=[employees.models.only_int])),
                ('account', models.CharField(max_length=25, null=True, validators=[employees.models.only_int])),
                ('operation', models.IntegerField(null=True)),
                ('pix', models.CharField(max_length=30, null=True)),
                ('date_admission', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('first_access', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='branches.branches')),
                ('epi', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='employees_epis.employeesepis')),
                ('pj_complements', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='pj_complements.pjcomplements')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'db_table': 'employees',
            },
        ),
    ]
