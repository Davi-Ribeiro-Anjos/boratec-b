# Generated by Django 3.2.19 on 2023-08-31 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epis_items', '0004_episitems_time_for_use'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episitems',
            name='ca',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]