# Generated by Django 4.0.6 on 2023-09-04 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
