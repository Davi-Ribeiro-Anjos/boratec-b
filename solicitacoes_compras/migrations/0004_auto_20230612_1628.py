# Generated by Django 3.2.19 on 2023-06-12 16:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes_compras', '0003_auto_20230531_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacoescompras',
            name='data_solicitacao_bo',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='solicitacoescompras',
            name='status',
            field=models.CharField(choices=[('ABERTO', 'Aberto'), ('ANDAMENTO', 'Andamento'), ('CONCLUIDO', 'Concluido'), ('CANCELADO', 'Cancelado')], default='ABERTO', max_length=30),
        ),
    ]
