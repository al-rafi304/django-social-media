# Generated by Django 4.2.1 on 2023-05-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hometown',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='occupation',
            field=models.CharField(max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='relationshipStatus',
            field=models.CharField(choices=[('SN', 'Single'), ('IR', 'In a relationship'), ('MR', 'Married'), ('CM', "It's complicated")], default=None, max_length=2, null=True),
        ),
    ]
