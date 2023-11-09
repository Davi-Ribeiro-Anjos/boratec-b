# Generated by Django 4.2.5 on 2023-11-09 13:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "payments_histories",
            "0002_paymentshistories_email_alter_paymentshistories_name",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymentshistories",
            name="data_emission",
        ),
        migrations.AddField(
            model_name="paymentshistories",
            name="subsistence_allowance",
            field=models.FloatField(default=0),
        ),
    ]
