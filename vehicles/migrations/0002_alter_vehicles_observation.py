# Generated by Django 3.2.19 on 2023-08-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='observation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]