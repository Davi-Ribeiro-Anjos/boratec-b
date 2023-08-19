# Generated by Django 3.2.19 on 2023-08-09 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('id_company', models.IntegerField()),
                ('id_branch', models.IntegerField()),
                ('id_garage', models.IntegerField(unique=True)),
                ('abbreviation', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('uf', models.CharField(max_length=2)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('company', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
                'db_table': 'branches',
            },
        ),
    ]
