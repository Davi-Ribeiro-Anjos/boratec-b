# Generated by Django 4.2.5 on 2023-10-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments_histories", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentshistories",
            name="email",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="paymentshistories",
            name="name",
            field=models.CharField(max_length=70),
        ),
    ]