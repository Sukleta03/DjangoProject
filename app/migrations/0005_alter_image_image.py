# Generated by Django 4.0.4 on 2023-05-31 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default='static/images/default.png', upload_to='static/images/'),
        ),
    ]
