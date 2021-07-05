# Generated by Django 3.1 on 2021-07-03 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0029_auto_20210703_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Refund_Paid', 'Refund_Paid')], default='Pending', max_length=25),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Refund_Paid', 'Refund_Paid')], default='Pending', max_length=25, null=True),
        ),
    ]
