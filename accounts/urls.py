from django.urls import re_path

from . import views

urlpatterns = [
    re_path('home', views.home,name='home-view'),
    re_path('managerment_user', views.managerment_user,name='managerment_user-view'),
    re_path('signup', views.signup_view,name='register_form_view'),
    re_path('login', views.login_view,name='login_form-view'),
    re_path('logout', views.logout_view,name='logout_form-view'),
]