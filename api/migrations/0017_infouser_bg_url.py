# Generated by Django 5.0.1 on 2024-01-31 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_rename_title_image_user_id_remove_image_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='infouser',
            name='bg_url',
            field=models.TextField(default=''),
        ),
    ]
