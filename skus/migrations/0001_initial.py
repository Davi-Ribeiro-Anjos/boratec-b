# Generated by Django 4.2.5 on 2023-10-04 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("xmls", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Skus",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("code", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=200)),
                ("type_unity", models.CharField(max_length=10)),
                ("quantity_unity", models.IntegerField()),
                ("type_volume", models.CharField(max_length=10)),
                ("quantity_volume", models.IntegerField()),
                (
                    "xml",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="skus",
                        to="xmls.xmls",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sku",
                "verbose_name_plural": "Skus",
                "db_table": "skus",
            },
        ),
    ]
