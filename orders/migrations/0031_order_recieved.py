# Generated by Django 3.1 on 2021-07-03 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_auto_20210703_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='recieved',
            field=models.BooleanField(default=False),
        ),
    ]
