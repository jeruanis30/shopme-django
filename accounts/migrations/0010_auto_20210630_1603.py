# Generated by Django 3.1 on 2021-06-30 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210630_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(blank=True, default='bugambilaya.jpg', null=True, upload_to='userprofile/'),
        ),
    ]