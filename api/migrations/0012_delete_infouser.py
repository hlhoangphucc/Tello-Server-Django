# Generated by Django 5.0.1 on 2024-01-31 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_inforuser_infouser_alter_infouser_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InfoUser',
        ),
    ]