# Generated by Django 5.1 on 2025-01-15 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0012_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='utype',
            field=models.CharField(default='employee', max_length=15),
        ),
    ]
