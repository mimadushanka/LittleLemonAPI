# Generated by Django 5.2.1 on 2025-05-30 17:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0002_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LittleLemonAPI.order'),
        ),
    ]
