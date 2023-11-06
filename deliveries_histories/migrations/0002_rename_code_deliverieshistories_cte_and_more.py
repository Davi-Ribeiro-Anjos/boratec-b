# Generated by Django 4.2.5 on 2023-10-16 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("branches", "0001_initial"),
        ("deliveries_histories", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deliverieshistories",
            old_name="code",
            new_name="cte",
        ),
        migrations.RenameField(
            model_name="deliverieshistories",
            old_name="date_forecast",
            new_name="lead_time",
        ),
        migrations.AddField(
            model_name="deliverieshistories",
            name="garage",
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="deliverieshistories",
            name="id_garage",
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="deliverieshistories",
            name="branch",
            field=models.ForeignKey(
                default=999,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deliveries_histories",
                to="branches.branches",
            ),
        ),
    ]