# Generated by Django 5.1.1 on 2024-11-11 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0023_merge_20241111_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='low_inventory_threshold',
        ),
    ]
