# Generated by Django 5.1 on 2025-01-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0013_employee_utype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_centre',
            name='utype',
            field=models.CharField(default='service_center', max_length=20),
        ),
    ]
