from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
 

class Message(models.Model):
    room_id = models.CharField(max_length=255)
    message = models.TextField()  # Trường lưu trữ hình ảnh
    sender_id = models.CharField(max_length=255)
    receiver_id = models.CharField(max_length=255)
    send_time = models.DateTimeField()
    message_type = models.CharField(max_length=255)
    voice_duration = models.CharField(max_length=255,default='Default voice')
    class Meta:
        db_table = 'messages'

class Video(models.Model):
    title = models.CharField(max_length=255, default='Default Title')
    video_file = models.FileField(upload_to='videos/')
    video_url = models.URLField(blank=True)
    class Meta:
        db_table = 'video'

class Image(models.Model):
    image_file = models.FileField(upload_to='images/')
    user_id=models.CharField(max_length=255,default='Default Title')
    class Meta:
        db_table = 'image'

class Voice(models.Model):
    title = models.CharField(max_length=255, default='Default Title')
    voice_file = models.FileField(upload_to='voices/')
    vocie_url = models.URLField(blank=True)
    voice_duration=models.TextField(default='Default Title')
    class Meta:
        db_table = 'voices'

class InfoUser(models.Model):
    user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    avt_url = models.TextField()  
    bg_url = models.TextField(default='')  
    upload_time = models.DateTimeField()
    class Meta:
        db_table = 'info_user'

class Posts(models.Model):
    post_id = models.CharField(max_length=255)
    text_post= models.TextField()  
    media_post = models.TextField()  
    user_name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255,default='Default Id')
    post_time = models.DateTimeField()
    post_type = models.CharField(max_length=255)
    class Meta:
        db_table = 'posts'
