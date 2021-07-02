# Generated by Django 3.1 on 2021-06-30 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20210630_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Accepted', 'Accepted'), ('New', 'New'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
