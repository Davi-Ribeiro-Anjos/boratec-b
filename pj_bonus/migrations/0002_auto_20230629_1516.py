# Generated by Django 3.2.19 on 2023-06-29 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pj_bonus', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pjbonus',
            options={'verbose_name': 'PJBonus', 'verbose_name_plural': 'PJBonus'},
        ),
        migrations.AlterModelTable(
            name='pjbonus',
            table='pj_bonus',
        ),
    ]
