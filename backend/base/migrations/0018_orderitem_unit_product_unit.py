# Generated by Django 4.2.1 on 2023-07-17 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0017_merge_20230717_1349"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="unit",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="unit",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]