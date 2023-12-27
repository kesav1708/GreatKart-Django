# Generated by Django 4.1.7 on 2023-12-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('New', 'New'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted')], default='New', max_length=100),
        ),
    ]