# Generated by Django 4.2.5 on 2023-11-22 10:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("vacancies_controls", "0007_vacanciescontrols_email_send_director_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vacanciescontrols",
            name="send_mail",
        ),
    ]