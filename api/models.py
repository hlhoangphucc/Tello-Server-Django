from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone


class InfoUser(models.Model):
    user_id = models.IntegerField(default=0, primary_key=True)
    user_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    gender = models.CharField(max_length=10, default="")
    avt_url = models.TextField()
    bg_url = models.TextField(default="")
    created_time = models.DateTimeField()
    online_time = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "info_user"


class Chatlists(models.Model):
    room_id = models.CharField(max_length=255, default="")
    last_msg = models.CharField(max_length=255, default="")
    my_name = models.CharField(max_length=255, default="")
    my_email = models.CharField(max_length=255, default="")
    my_id = models.ForeignKey(
        InfoUser,
        on_delete=models.CASCADE,
        db_column="my_user_id",
        default=0,
        related_name="my_chatlists",
    )
    other_id = models.ForeignKey(
        InfoUser,
        on_delete=models.CASCADE,
        db_column="other_user_id",
        default=0,
        related_name="other_chatlists",
    )
    name_other = models.CharField(max_length=255, default="")
    email_other = models.CharField(max_length=255, default="")
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "chatlist"


class Message(models.Model):
    room_id = models.CharField(max_length=255, default="")
    message = models.TextField()
    sender_id = models.ForeignKey(
        InfoUser,
        on_delete=models.CASCADE,
        db_column="sender_id",
        default=0,
        related_name="sent_messages",
    )
    receiver_id = models.ForeignKey(
        InfoUser,
        on_delete=models.CASCADE,
        db_column="receiver_id",
        default=0,
        related_name="received_messages",
    )
    send_time = models.DateTimeField()
    message_type = models.CharField(max_length=255)
    voice_duration = models.CharField(max_length=255, default="Default voice")

    class Meta:
        db_table = "messages"


class Posts(models.Model):
    post_id = models.CharField(max_length=255, primary_key=True)
    text_post = models.TextField()
    media_post = models.TextField(null=True)
    user_name = models.CharField(max_length=255)
    avt_user = models.CharField(max_length=255, default="")
    user_id = models.ForeignKey(
        InfoUser, on_delete=models.CASCADE, db_column="post_user_id", default=0
    )
    post_time = models.DateTimeField()
    post_type = models.CharField(max_length=255)
    is_edit = models.BooleanField(default=False)

    class Meta:
        db_table = "posts"


class Interact(models.Model):
    post_id = models.OneToOneField(
        Posts,
        on_delete=models.CASCADE,
        db_column="post_id",
        max_length=255,
        default="",
        primary_key=True,
    )
    user_id = models.ForeignKey(
        InfoUser, on_delete=models.CASCADE, db_column="user_id", default=0
    )
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "interact"


class Comments(models.Model):
    post_id = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        db_column="post_id",
        max_length=255,
        default="",
    )
    user_id = models.ForeignKey(
        InfoUser, on_delete=models.CASCADE, db_column="user_id", default=0
    )
    creatd_at = models.DateTimeField()
    content_comment = models.TextField()
    is_edit = models.BooleanField(default=False)

    class Meta:
        db_table = "comments"


class Follows(models.Model):
    my_user_id = models.ForeignKey(
        InfoUser,
        on_delete=models.CASCADE,
        db_column="sent_follow",
        default=0,
        related_name="follows_sent",
    )
    other_user_id = models.ForeignKey(
        InfoUser,
        on_delete=models.CASCADE,
        db_column="receiver_follow",
        default=0,
        related_name="follows_received",
    )

    class Meta:
        db_table = "follows"


class Video(models.Model):
    title = models.CharField(max_length=255, default="Default Title")
    video_file = models.FileField(upload_to="video/")
    video_url = models.URLField(blank=True)

    class Meta:
        db_table = "video"


class Image(models.Model):
    image_file = models.FileField(upload_to="images/")
    user_id = models.CharField(max_length=255, default="Default Title")

    class Meta:
        db_table = "image"


class Media(models.Model):
    title = models.CharField(max_length=255, default="Default Title")
    media_file = models.FileField(upload_to="all/")
    media_url = models.URLField(blank=True)

    class Meta:
        db_table = "media"


class Voice(models.Model):
    title = models.CharField(max_length=255, default="Default Title")
    voice_file = models.FileField(upload_to="voices/")
    vocie_url = models.URLField(blank=True)
    voice_duration = models.TextField(default="Default Title")

    class Meta:
        db_table = "voices"
