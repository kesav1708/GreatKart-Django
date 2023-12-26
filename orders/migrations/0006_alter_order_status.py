# Generated by Django 5.0 on 2023-12-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0005_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Completed", "Completed"),
                    ("Accepted", "Accepted"),
                    ("Cancelled", "Cancelled"),
                    ("New", "New"),
                ],
                default="New",
                max_length=100,
            ),
        ),
    ]
