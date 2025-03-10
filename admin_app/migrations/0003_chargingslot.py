# Generated by Django 5.1 on 2025-01-28 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_rename_image_chargingstations_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_booked', models.BooleanField(default=False)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='admin_app.chargingstations')),
            ],
        ),
    ]
