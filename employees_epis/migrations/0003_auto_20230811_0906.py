# Generated by Django 3.2.19 on 2023-08-11 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees_epis', '0002_employeesepis_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesepis',
            name='notebook_code',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='employeesepis',
            name='phone_code',
            field=models.IntegerField(null=True),
        ),
    ]
