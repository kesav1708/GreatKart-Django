# Generated by Django 5.0 on 2023-12-25 09:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_productgallery"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ProductGallery",
        ),
    ]