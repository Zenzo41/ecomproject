# Generated by Django 4.2.2 on 2023-08-21 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ecomapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("Order Received", "Order Received"),
                    ("Order Completed", "Order Completed"),
                    ("Order Cancelled", "Order Cancelled"),
                ],
                max_length=50,
            ),
        ),
    ]