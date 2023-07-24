# Generated by Django 3.2.19 on 2023-07-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filiais',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('id_empresa', models.IntegerField()),
                ('id_filial', models.IntegerField()),
                ('id_garagem', models.IntegerField(unique=True)),
                ('sigla', models.CharField(max_length=3, unique=True)),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('uf', models.CharField(max_length=2)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
            ],
            options={
                'verbose_name': 'Filial',
                'verbose_name_plural': 'Filiais',
                'db_table': 'filiais',
            },
        ),
    ]
