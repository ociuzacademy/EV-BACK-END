# Generated by Django 5.1 on 2025-01-06 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0007_repair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='status',
            field=models.CharField(default='repair_requested', max_length=50),
        ),
    ]
