# Generated by Django 5.1 on 2025-01-13 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0009_remove_service_centre_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service_centre',
            old_name='latitutde',
            new_name='latitude',
        ),
        migrations.RemoveField(
            model_name='service_centre',
            name='owner_name',
        ),
    ]
