# Generated by Django 5.1 on 2025-01-20 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0017_products_service_centre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(),
        ),
    ]
