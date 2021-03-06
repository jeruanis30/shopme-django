# Generated by Django 3.1 on 2021-06-26 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=51),
        ),
        migrations.AddField(
            model_name='account',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=51),
        ),
        migrations.AddField(
            model_name='account',
            name='city',
            field=models.CharField(blank=True, max_length=54),
        ),
        migrations.AddField(
            model_name='account',
            name='country',
            field=models.CharField(blank=True, max_length=54),
        ),
        migrations.AddField(
            model_name='account',
            name='state',
            field=models.CharField(blank=True, max_length=54),
        ),
    ]
