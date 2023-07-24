# Generated by Django 3.2.19 on 2023-07-24 11:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PJComplementos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('salario', models.FloatField()),
                ('ajuda_custo', models.FloatField(default=0)),
                ('faculdade', models.FloatField(default=0)),
                ('credito_convenio', models.FloatField(default=0)),
                ('auxilio_moradia', models.FloatField(default=0)),
                ('outros_creditos', models.FloatField(default=0)),
                ('adiantamento', models.FloatField(default=0)),
                ('desconto_convenio', models.FloatField(default=0)),
                ('outros_descontos', models.FloatField(default=0)),
                ('data_pagamento', models.DateField()),
                ('data_emissao', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'PJComplemento',
                'verbose_name_plural': 'PJComplementos',
                'db_table': 'pj_complementos',
            },
        ),
    ]
