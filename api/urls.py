from django.urls import re_path

from . import views

urlpatterns = [
    re_path("signup", views.signup),
    re_path("login", views.login),
    re_path("test_token", views.test_token),
    re_path("get_all_user", views.get_all_user),
    re_path(r"^get_user/(?P<user_id>.+)/$", views.get_user, name="get_user"),
    re_path("get_authenticated_user", views.get_authenticated_user),
    re_path("upload_posts", views.UploadPosts, name="upload_posts"),
    re_path("upload_media", views.UploadMedia, name="upload_media"),
    re_path("upload_voice", views.UploadVoiceMessageVoice, name="upload_voice"),
    re_path("update_avt", views.UpdateAvt, name="update_avt"),
    re_path("update_post", views.UpdatePost, name="update_post"),
    re_path("get_all_posts", views.GetAllPost, name="get_all_posts"),
    re_path("get_post_user", views.GetPostFromUser, name="get_all_posts"),
    re_path("add_like", views.AddLike, name="add_like"),
    re_path("un_like", views.UnLike, name="un_like"),
    re_path("add_comment", views.Comment, name="add_comment"),
    re_path("get_comment", views.GetCommentFromPostId, name="get_comment"),
    re_path(
        r"^delete_comment/(?P<id>.+)/$",
        views.DeleteComment,
        name="delete_comment",
    ),
    re_path("update_comment", views.UpdateComment, name="update_comment"),
    re_path("add_follow", views.FollowUser, name="add_follow"),
    re_path("un_follow", views.UnFollow, name="un_follow"),
    re_path("get_follow", views.GetFollowUser, name="get_follow"),
    re_path(r"^delete_post/(?P<post_id>.+)/$", views.DeletePost, name="delete_post"),
    re_path(r"^get_video/(?P<video_path>.+)$", views.GetVideoView, name="get_video"),
    re_path(r"^get_image/(?P<image_path>.+)$", views.GetImageView, name="get_image"),
    re_path(r"^get_voice/(?P<voice_path>.+)$", views.GetVoiceView, name="get_voice"),
    re_path(r"^get_media/(?P<media_path>.+)$", views.GetMedia, name="get_media"),
]
