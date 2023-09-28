# Generated by Django 4.2.5 on 2023-09-27 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0001_initial"),
        ("purchases_requests", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchasesrequests",
            name="requester",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="purchases_requesters",
                to="employees.employees",
            ),
        ),
    ]
