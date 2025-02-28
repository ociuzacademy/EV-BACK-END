# Generated by Django 5.1 on 2025-01-15 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0011_rename_longitutde_service_centre_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50, unique=True)),
                ('name', models.CharField(default='', max_length=50)),
                ('email', models.CharField(default='', max_length=100)),
                ('phone_number', models.CharField(default='', max_length=15)),
                ('password', models.CharField(default='', max_length=50)),
                ('service_centre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_app.service_centre')),
            ],
        ),
    ]
