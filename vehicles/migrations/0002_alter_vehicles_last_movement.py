# Generated by Django 3.2.19 on 2023-09-06 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='last_movement',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
