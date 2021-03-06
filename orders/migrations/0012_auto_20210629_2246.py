# Generated by Django 3.1 on 2021-06-29 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20210629_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='ip',
            field=models.CharField(blank=True, max_length=21),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted'), ('New', 'New')], default='New', max_length=10),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Refund_Paid', 'Refund_Paid')], default='Pending', max_length=200, null=True),
        ),
    ]
