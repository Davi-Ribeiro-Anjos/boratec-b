# Generated by Django 3.2.19 on 2023-09-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_remove_clientsbranches_type_pallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsbranches',
            name='type_pallet',
            field=models.CharField(choices=[('PBR', 'Pbr'), ('CHEP', 'Chep')], default='PBR', max_length=4),
        ),
    ]
