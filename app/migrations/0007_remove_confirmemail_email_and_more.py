# Generated by Django 4.0.4 on 2023-06-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirmemail',
            name='email',
        ),
        migrations.RemoveField(
            model_name='confirmemail',
            name='password',
        ),
        migrations.AddField(
            model_name='confirmemail',
            name='email_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
