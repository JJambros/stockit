# Generated by Django 5.1.1 on 2024-10-13 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('db', '0008_alter_audittrail_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audittrail',
            name='inventory',
        ),
        migrations.RemoveField(
            model_name='audittrail',
            name='order',
        ),
        migrations.AddField(
            model_name='audittrail',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='audittrail',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='contact_phone',
            field=models.CharField(max_length=20),
        ),
    ]