# Generated by Django 3.2.19 on 2023-06-01 12:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes_entradas', '0002_rename_obs_solicitacoesentradas_observacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacoesentradas',
            name='data_criacao',
            field=models.DateField(default=datetime.date(2023, 6, 1)),
        ),
    ]
