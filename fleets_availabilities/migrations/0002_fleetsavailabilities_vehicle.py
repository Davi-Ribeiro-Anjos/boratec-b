# Generated by Django 3.2.19 on 2023-08-18 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicles', '0001_initial'),
        ('fleets_availabilities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fleetsavailabilities',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fleets_availabilities', to='vehicles.vehicles'),
        ),
    ]
