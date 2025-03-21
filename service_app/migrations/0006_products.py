# Generated by Django 5.1 on 2025-01-02 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0005_alter_service_centre_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity', models.CharField(default='', max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
            ],
        ),
    ]
