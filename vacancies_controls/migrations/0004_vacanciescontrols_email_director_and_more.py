# Generated by Django 4.2.5 on 2023-11-17 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vacancies_controls", "0003_alter_vacanciescontrols_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="vacanciescontrols",
            name="email_director",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="vacanciescontrols",
            name="email_manager",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="vacanciescontrols",
            name="email_regional_manager",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="vacanciescontrols",
            name="email_rh",
            field=models.CharField(max_length=100, null=True),
        ),
    ]