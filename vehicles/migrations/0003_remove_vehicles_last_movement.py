# Generated by Django 3.2.19 on 2023-09-06 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0002_alter_vehicles_last_movement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicles',
            name='last_movement',
        ),
    ]