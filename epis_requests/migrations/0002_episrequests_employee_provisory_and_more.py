# Generated by Django 4.2.5 on 2023-09-26 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0001_initial"),
        ("epis_requests", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="episrequests",
            name="employee_provisory",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="episrequests",
            name="employee",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="epis_requests",
                to="employees.employees",
            ),
        ),
    ]