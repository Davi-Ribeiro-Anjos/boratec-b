# Generated by Django 3.2.19 on 2023-08-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees_epis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeesepis',
            name='observation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
