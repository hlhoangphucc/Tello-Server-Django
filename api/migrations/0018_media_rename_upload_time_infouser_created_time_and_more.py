# Generated by Django 5.0.1 on 2024-03-07 09:32

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_infouser_bg_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Default Title', max_length=255)),
                ('media_file', models.FileField(upload_to='all/')),
                ('media_url', models.URLField(blank=True)),
            ],
            options={
                'db_table': 'media',
            },
        ),
        migrations.RenameField(
            model_name='infouser',
            old_name='upload_time',
            new_name='created_time',
        ),
        migrations.RemoveField(
            model_name='infouser',
            name='id',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='id',
        ),
        migrations.AddField(
            model_name='infouser',
            name='email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='infouser',
            name='gender',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='infouser',
            name='online_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='infouser',
            name='phone',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='infouser',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='posts',
            name='avt_user',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='posts',
            name='is_edit',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='infouser',
            name='user_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver_id',
            field=models.ForeignKey(db_column='receiver_id', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='api.infouser'),
        ),
        migrations.AlterField(
            model_name='message',
            name='room_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_id',
            field=models.ForeignKey(db_column='sender_id', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='api.infouser'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='media_post',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='posts',
            name='user_id',
            field=models.ForeignKey(db_column='post_user_id', default=0, on_delete=django.db.models.deletion.CASCADE, to='api.infouser'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(upload_to='video/'),
        ),
        migrations.CreateModel(
            name='Chatlists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(default='', max_length=255)),
                ('last_msg', models.CharField(default='', max_length=255)),
                ('my_name', models.CharField(default='', max_length=255)),
                ('my_email', models.CharField(default='', max_length=255)),
                ('name_other', models.CharField(default='', max_length=255)),
                ('email_other', models.CharField(default='', max_length=255)),
                ('updated_at', models.DateTimeField()),
                ('my_id', models.ForeignKey(db_column='my_user_id', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='my_chatlists', to='api.infouser')),
                ('other_id', models.ForeignKey(db_column='other_user_id', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='other_chatlists', to='api.infouser')),
            ],
            options={
                'db_table': 'chatlist',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creatd_at', models.DateTimeField()),
                ('content_comment', models.TextField()),
                ('is_edit', models.BooleanField(default=False)),
                ('post_id', models.ForeignKey(db_column='post_id', default='', max_length=255, on_delete=django.db.models.deletion.CASCADE, to='api.posts')),
                ('user_id', models.ForeignKey(db_column='user_id', default=0, on_delete=django.db.models.deletion.CASCADE, to='api.infouser')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_user_id', models.ForeignKey(db_column='sent_follow', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='follows_sent', to='api.infouser')),
                ('other_user_id', models.ForeignKey(db_column='receiver_follow', default=0, on_delete=django.db.models.deletion.CASCADE, related_name='follows_received', to='api.infouser')),
            ],
            options={
                'db_table': 'follows',
            },
        ),
        migrations.CreateModel(
            name='Interact',
            fields=[
                ('post_id', models.OneToOneField(db_column='post_id', default='', max_length=255, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.posts')),
                ('updated_at', models.DateTimeField()),
                ('user_id', models.ForeignKey(db_column='user_id', default=0, on_delete=django.db.models.deletion.CASCADE, to='api.infouser')),
            ],
            options={
                'db_table': 'interact',
            },
        ),
    ]
