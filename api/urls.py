from django.urls import re_path

from . import views

urlpatterns = [
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('test_token', views.test_token),
    re_path('get_all',views.get_all),
    re_path('get_authenticated_user',views.get_authenticated_user),
    re_path('upload_image', views.UploadImage, name='upload_image'),
    re_path('upload_video', views.UploadVideoToMessage, name='upload_video'),
    re_path('upload_voice', views.UploadVoiceMessageVoice, name='upload_voice'),
    re_path('update_avt', views.UpdateAvt, name='update_avt'),


    re_path(r'^get_video/(?P<video_path>.+)$',views.GetVideoView, name='get_video'),
    re_path(r'^get_image/(?P<image_path>.+)$',views.GetImageView, name='get_image'),
    re_path(r'^get_voice/(?P<voice_path>.+)$',views.GetVoiceView, name='get_voice'),
]
