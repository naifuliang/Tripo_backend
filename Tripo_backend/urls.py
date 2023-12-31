"""Tripo_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path

import authorization.views
from authorization import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from tripo_main_interface import views as main_views
from image_manager import views as img_views
from django.views.static import serve
from . import settings

from django.conf.urls.static import static

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path(r'media/(?P<path>.*)', serve,{'document_root': settings.MEDIA_ROOT}),
    path("verification/", auth_views.verification.as_view(), name='verification'),
    path("register/", auth_views.register.as_view(), name='register'),
    path("reset/", auth_views.reset.as_view(), name='reset'),
    path('api/token/', authorization.views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('get_user_info/', main_views.get_user_info.as_view(), name='get_user_info'),
    path('set_user_info/', main_views.set_user_info.as_view(), name='set_user_info'),
    path('upload_avatar/', main_views.upload_user_avatar.as_view(), name='upload_avatar'),
    path('get_post/', main_views.get_post.as_view(), name='get_post'),
    path('publish/', main_views.publish_post.as_view(), name='push_post_info'),
    path('upload_images/', main_views.upload_images.as_view(), name='upload_images'),
    path('modify_post/', main_views.modify_post.as_view(), name='set_post_info'),
    path('delete_post/', main_views.delete_post.as_view(), name='delete_post_info'),
    path('post_list/', main_views.post_list.as_view(), name='post_list'),
    path('like/', main_views.like.as_view(), name='like'),
    path('comment/', main_views.comment.as_view(), name='comment'),
    path('message/', main_views.get_message.as_view(), name='message'),
    path('nearby/', main_views.nearby.as_view(), name='nearby'),
    path('get_chat_response/', main_views.get_chat_response.as_view(), name='get_chat_response'),
    path('AI_conclusion/', main_views.AI_conclusion.as_view(), name='AI_conclusion'),
    path('get_tags/', main_views.get_tags.as_view(), name='get_tags'),
    path('generate_tags/', main_views.generate_tags.as_view(), name='get_tags'),

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
