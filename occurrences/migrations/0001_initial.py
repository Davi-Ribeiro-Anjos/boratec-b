# Generated by Django 4.2.5 on 2023-11-03 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("branches", "0001_initial"),
        ("deliveries_histories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Occurrences",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
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
