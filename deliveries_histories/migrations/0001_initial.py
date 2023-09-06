# Generated by Django 3.2.19 on 2023-09-05 15:12

import deliveries_histories.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveriesHistories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('code', models.CharField(max_length=15, validators=[deliveries_histories.models.only_int])),
                ('date_emission', models.DateField()),
                ('date_forecast', models.DateField()),
                ('date_delivery', models.DateField()),
                ('recipient', models.CharField(max_length=200)),
                ('sender', models.CharField(max_length=200)),
                ('delivery_location', models.CharField(max_length=100)),
                ('weight', models.FloatField(default=0)),
                ('opened', models.SmallIntegerField(default=0)),
                ('nf', models.TextField()),
                ('document_type', models.CharField(choices=[('NFS', 'Nfs'), ('CTE', 'Cte')], max_length=3)),
                ('description_justification', models.CharField(choices=[('FERIADO NACIONAL', 'Feriado Nacional'), ('FERIADOS MUNICIPAIS / ESTADUAIS', 'Feriados Municipais Estaduais'), ('ENTREGA AGENDADA', 'Entrega Agendada'), ('CLIENTE COM RETENÇÃO FISCAL', 'Cliente Com Retenção Fiscal'), ('DESTINATARIO NÃO RECEBEU O XML', 'Destinatario Não Recebeu O Xml'), ('NF SEM PEDIDO', 'Nf Sem Pedido'), ('PEDIDO EXPIRADO', 'Pedido Expirado'), ('EXCESSO DE VEICULOS', 'Excesso De Veiculos'), ('GRADE FIXA', 'Grade Fixa'), ('DEVOLUÇÃO TOTAL ', 'Devolução Total'), ('ATRASO NA TRANSFERENCIA', 'Atraso Na Transferencia'), ('CUSTO', 'Custo'), ('ENTREGUE SEM LEAD TIME', 'Entregue Sem Lead Time')], max_length=50, null=True)),
                ('file', models.FileField(null=True, upload_to='justification/%Y/%m/%d')),
                ('confirmed', models.BooleanField(default=False)),
                ('refuse', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deliveries_histories', to='employees.employees')),
                ('branch', models.ForeignKey(default=99, on_delete=django.db.models.deletion.CASCADE, related_name='deliveries_histories', to='branches.branches')),
            ],
            options={
                'verbose_name': 'DeliveryHistory',
                'verbose_name_plural': 'DeliveriesHistories',
                'db_table': 'deliveries_histories',
            },
        ),
    ]
