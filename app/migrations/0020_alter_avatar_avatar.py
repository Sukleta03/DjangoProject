# Generated by Django 3.2.20 on 2023-09-04 14:11

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_avatar_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='avatar',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='avatar'),
        ),
    ]
