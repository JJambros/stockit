# Generated by Django 5.1.2 on 2024-11-14 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0025_merge_20241113_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='category',
        ),
    ]
