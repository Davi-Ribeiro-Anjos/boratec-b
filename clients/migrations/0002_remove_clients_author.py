# Generated by Django 3.2.19 on 2023-09-06 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='author',
        ),
    ]