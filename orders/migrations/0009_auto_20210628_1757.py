# Generated by Django 3.1 on 2021-06-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20210628_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('New', 'New'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
