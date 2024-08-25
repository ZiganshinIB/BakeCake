# Generated by Django 4.2.15 on 2024-08-25 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cake", "0006_cake_image_alter_order_delivered_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cake",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Стоимость",
            ),
        ),
    ]
