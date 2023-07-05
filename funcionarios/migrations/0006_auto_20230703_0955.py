# Generated by Django 3.2.19 on 2023-07-03 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pj_complementos', '0007_auto_20230703_0955'),
        ('funcionarios_epis', '0001_initial'),
        ('funcionarios', '0005_auto_20230629_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionarios',
            name='complemento_funcionario',
        ),
        migrations.AddField(
            model_name='funcionarios',
            name='epi',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to='funcionarios_epis.funcionariosepis'),
        ),
        migrations.AddField(
            model_name='funcionarios',
            name='pj_complementos',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to='pj_complementos.pjcomplementos'),
        ),
    ]
