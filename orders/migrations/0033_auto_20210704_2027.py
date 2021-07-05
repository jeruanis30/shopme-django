# Generated by Django 3.1 on 2021-07-04 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_order_item_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Refund_Paid', 'Refund_Paid'), ('Deleted', 'Deleted')], default='Pending', max_length=25),
        ),
    ]
