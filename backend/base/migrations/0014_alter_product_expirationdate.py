# Generated by Django 4.2.1 on 2023-07-08 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0013_product_expirationdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="expirationDate",
            field=models.DateField(blank=True, default="2023-12-12", null=True),
        ),
    ]