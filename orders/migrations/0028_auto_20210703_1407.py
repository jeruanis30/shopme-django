# Generated by Django 3.1 on 2021-07-03 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0027_auto_20210703_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Completed', 'Completed'), ('New', 'New'), ('Accepted', 'Accepted')], default='New', max_length=10),
        ),
    ]
