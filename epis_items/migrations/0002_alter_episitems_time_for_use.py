# Generated by Django 3.2.19 on 2023-09-06 12:23

from django.db import migrations, models
import epis_items.models


class Migration(migrations.Migration):

    dependencies = [
        ('epis_items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episitems',
            name='time_for_use',
            field=models.CharField(blank=True, default=365, max_length=3, null=True, validators=[epis_items.models.only_int]),
        ),
    ]