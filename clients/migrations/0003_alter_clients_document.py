# Generated by Django 3.2.19 on 2023-09-02 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_clients_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='document',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
