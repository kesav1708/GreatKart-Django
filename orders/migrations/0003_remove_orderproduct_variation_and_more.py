# Generated by Django 5.0 on 2023-12-22 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_remove_orderproduct_color_remove_orderproduct_size_and_more"),
        ("store", "0002_variation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderproduct",
            name="variation",
        ),
        migrations.AddField(
            model_name="orderproduct",
            name="variations",
            field=models.ManyToManyField(blank=True, to="store.variation"),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Accepted", "Accepted"),
                    ("Completed", "Completed"),
                    ("Cancelled", "Cancelled"),
                    ("New", "New"),
                ],
                default="New",
                max_length=100,
            ),
        ),
    ]
