# Generated by Django 5.1.2 on 2024-11-11 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0022_merge_20241111_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='low_inventory_threshold',
        ),
    ]