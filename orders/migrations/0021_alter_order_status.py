# Generated by Django 4.1.7 on 2023-12-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed'), ('New', 'New')], default='New', max_length=100),
        ),
    ]
