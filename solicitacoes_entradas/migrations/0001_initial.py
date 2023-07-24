# Generated by Django 3.2.19 on 2023-07-24 11:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('funcionarios', '0001_initial'),
        ('solicitacoes_compras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacoesEntradas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('observacao', models.TextField()),
                ('arquivo_1', models.FileField(blank=True, null=True, upload_to='compras/%Y/%m/%d')),
                ('arquivo_2', models.FileField(blank=True, null=True, upload_to='compras/%Y/%m/%d')),
                ('arquivo_3', models.FileField(blank=True, null=True, upload_to='compras/%Y/%m/%d')),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_entradas', to='funcionarios.funcionarios')),
                ('solicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitacoes_compras.solicitacoescompras')),
            ],
            options={
                'verbose_name': 'SolicitacaoEntrada',
                'verbose_name_plural': 'SolicitacoesEntradas',
                'db_table': 'solicitacoes_entradas',
            },
        ),
    ]
