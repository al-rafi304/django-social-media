# Generated by Django 4.2.1 on 2023-05-22 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_hometown_alter_account_occupation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='fName',
        ),
        migrations.RemoveField(
            model_name='account',
            name='lName',
        ),
    ]
