# Generated by Django 4.2.5 on 2023-10-16 16:07

from django.db import migrations, models
import django.db.models.deletion
import occurrences.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("branches", "0001_initial"),
        ("deliveries_histories", "0002_rename_code_deliverieshistories_cte_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Occurrences",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                (
                    "cte",
                    models.CharField(max_length=15),
                ),
                ("garage", models.CharField(max_length=5)),
                ("date_emission", models.DateField()),
                (
                    "document_type",
                    models.CharField(
                        choices=[("NFS", "Nfs"), ("CTE", "Cte")], max_length=3
                    ),
                ),
                ("occurrence_code", models.CharField(max_length=5)),
                ("occurrence_description", models.CharField(max_length=200)),
                (
                    "branch",
                    models.ForeignKey(
                        default=999,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="occurrences",
                        to="branches.branches",
                    ),
                ),
                (
                    "justification",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="occurrences",
                        to="deliveries_histories.deliverieshistories",
                    ),
                ),
            ],
            options={
                "verbose_name": "Occurrence",
                "verbose_name_plural": "Occurrences",
                "db_table": "occurrences",
            },
        ),
    ]
