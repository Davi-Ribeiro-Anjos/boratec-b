# Generated by Django 3.2.19 on 2023-08-09 10:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchasesRequests',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('number_request', models.IntegerField(unique=True)),
                ('date_request', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_expiration', models.DateField(blank=True, null=True)),
                ('date_completion', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ABERTO', 'Aberto'), ('ANDAMENTO', 'Andamento'), ('CONCLUIDO', 'Concluido'), ('CANCELADO', 'Cancelado')], default='ABERTO', max_length=30)),
                ('department', models.CharField(blank=True, choices=[('NAO INFORMADO', 'Default'), ('DIRETORIA', 'Diretoria'), ('FATURAMENTO', 'Faturamento'), ('FINANCEIRO', 'Financeiro'), ('RH', 'Rh'), ('FISCAL', 'Fiscal'), ('MONITORAMENTO', 'Monitoramento'), ('OPERACIONAL', 'Operacional'), ('FROTA', 'Frota'), ('EXPEDICAO', 'Expedicao'), ('COMERCIAL', 'Comercial'), ('JURIDICO', 'Juridico'), ('DESENVOLVIMENTO', 'Desenvolvimento'), ('TI', 'Ti'), ('FILIAIS', 'Filiais'), ('COMPRAS', 'Compras')], default='NAO INFORMADO', max_length=30, null=True)),
                ('category', models.CharField(blank=True, choices=[('NAO INFORMADO', 'Default'), ('ALMOXARIFADO', 'Almoxarifado'), ('COTACAO', 'Cotacao'), ('NOTA FISCAL', 'Nota Fiscal')], default='NAO INFORMADO', max_length=30, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('NAO INFORMADO', 'Default'), ('A VISTA', 'A Vista'), ('PARCELADO 1X', 'Parcelado 1X'), ('PARCELADO 2X', 'Parcelado 2X'), ('PARCELADO 3X', 'Parcelado 3X'), ('PARCELADO 4X', 'Parcelado 4X'), ('PARCELADO 5X', 'Parcelado 5X'), ('PARCELADO 6X', 'Parcelado 6X'), ('PARCELADO 7X', 'Parcelado 7X'), ('PARCELADO 8X', 'Parcelado 8X'), ('PARCELADO 9X', 'Parcelado 9X'), ('PARCELADO 10X', 'Parcelado 10X'), ('PARCELADO 11X', 'Parcelado 11X'), ('PARCELADO 12X', 'Parcelado 12X')], default='NAO INFORMADO', max_length=30, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('observation', models.TextField(blank=True, null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='purchases_requests/%Y/%m/%d')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_author', to='employees.employees')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchases_requests', to='branches.branches')),
                ('latest_updater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_latest_updater', to='employees.employees')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_requester', to='employees.employees')),
                ('responsible', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchase_responsible', to='employees.employees')),
            ],
            options={
                'verbose_name': 'PurchaseRequest',
                'verbose_name_plural': 'PurchasesRequests',
                'db_table': 'purchases_requests',
            },
        ),
    ]
