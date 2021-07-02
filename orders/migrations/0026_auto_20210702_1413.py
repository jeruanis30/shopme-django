# Generated by Django 3.1 on 2021-07-02 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_auto_20210702_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted')], default='New', max_length=10),
        ),
    ]
