# Generated by Django 3.2.19 on 2023-05-31 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes_compras', '0003_auto_20230531_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacoescompras',
            name='data_solicitacao_bo',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 31, 17, 9, 1, 888566)),
        ),
    ]
