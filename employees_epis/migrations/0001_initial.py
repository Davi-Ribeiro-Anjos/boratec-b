# Generated by Django 3.2.19 on 2023-08-09 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeesEPIs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('phone_model', models.CharField(max_length=50, null=True)),
                ('phone_code', models.IntegerField(null=True, unique=True)),
                ('notebook_model', models.CharField(max_length=50, null=True)),
                ('notebook_code', models.IntegerField(null=True, unique=True)),
            ],
            options={
                'verbose_name': 'EmployeeEPI',
                'verbose_name_plural': 'EmployeesEPIs',
                'db_table': 'employees_epis',
            },
        ),
    ]
