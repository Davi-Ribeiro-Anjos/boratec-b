# Generated by Django 4.2.5 on 2023-12-05 10:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("branches", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="branches",
            name="name",
            field=models.CharField(max_length=50),
        ),
    ]
