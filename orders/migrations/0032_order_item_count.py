# Generated by Django 3.1 on 2021-07-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0031_order_recieved'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item_count',
            field=models.IntegerField(null=True),
        ),
    ]
