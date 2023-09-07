# Generated by Django 3.2.19 on 2023-09-05 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EPIsGroups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epis_groups', to='employees.employees')),
            ],
            options={
                'verbose_name': 'EPIGroup',
                'verbose_name_plural': 'EPIsGroups',
                'db_table': 'epis_groups',
            },
        ),
    ]
