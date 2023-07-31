# Generated by Django 3.2.19 on 2023-07-29 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0007_alter_funcionarios_genero'),
        ('solicitacoes_compras', '0004_auto_20230612_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacoescompras',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras_autor', to='funcionarios.funcionarios'),
        ),
        migrations.AlterField(
            model_name='solicitacoescompras',
            name='responsavel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='compras_responsavel', to='funcionarios.funcionarios'),
        ),
        migrations.AlterField(
            model_name='solicitacoescompras',
            name='solicitante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='compras_solicitante', to='funcionarios.funcionarios'),
        ),
        migrations.AlterField(
            model_name='solicitacoescompras',
            name='ultima_atualizacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras_ultima_att', to='funcionarios.funcionarios'),
        ),
    ]
