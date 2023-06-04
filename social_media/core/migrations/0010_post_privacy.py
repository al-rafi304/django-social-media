# Generated by Django 4.2.1 on 2023-06-01 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_post_sharecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.CharField(choices=[('EV', 'Everyone'), ('FL', 'Followers')], default='EV', max_length=2),
        ),
    ]