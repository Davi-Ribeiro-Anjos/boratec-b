# Generated by Django 3.2.19 on 2023-09-06 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleets_availabilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fleetsavailabilities',
            name='status',
            field=models.CharField(choices=[('PARADO', 'Parado'), ('PREVENTIVO', 'Preventivo'), ('FUNCIONANDO', 'Funcionando')], max_length=11),
        ),
    ]
