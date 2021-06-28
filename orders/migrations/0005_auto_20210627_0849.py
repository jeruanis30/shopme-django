# Generated by Django 3.1 on 2021-06-27 00:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0004_auto_20210626_2113'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order_Product',
            new_name='OrderProduct',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Completed', 'Completed'), ('New', 'New'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
