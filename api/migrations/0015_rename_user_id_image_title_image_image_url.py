# Generated by Django 5.0.1 on 2024-01-31 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_rename_title_image_user_id_remove_image_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='user_id',
            new_name='title',
        ),
        migrations.AddField(
            model_name='image',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]