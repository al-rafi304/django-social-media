# Generated by Django 4.2.1 on 2023-05-27 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_account_fname_remove_account_lname'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='cover_img',
            field=models.ImageField(blank=True, null=True, upload_to='cover_pics/'),
        ),
        migrations.AddField(
            model_name='account',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='account',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='dob',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='hometown',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='occupation',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]