# Generated by Django 5.0 on 2023-12-19 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Variation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "variation_category",
                    models.CharField(
                        choices=[("color", "color"), ("size", "size")], max_length=100
                    ),
                ),
                ("variation_value", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
            ],
        ),
    ]
