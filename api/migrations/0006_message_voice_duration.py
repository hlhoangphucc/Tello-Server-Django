# Generated by Django 5.0.1 on 2024-01-31 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_voice_voice_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='voice_duration',
            field=models.CharField(default='Default voice', max_length=255),
        ),
    ]
