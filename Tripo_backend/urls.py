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

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path("verification/", auth_views.verification.as_view(), name='verification'),
    path("register/", auth_views.register.as_view(), name='register'),
    path("reset/", auth_views.reset.as_view(), name='reset'),
    path('api/token/', authorization.views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('get_user_info/', main_views.get_user_info.as_view(), name='get_user_info'),
    path('set_user_info/', main_views.set_user_info.as_view(), name='set_user_info'),
    path('get_post_info/', main_views.get_post_info.as_view(), name='get_post_info'),
    path('push_post_info/', main_views.push_post_info.as_view(), name='push_post_info'),
    path('set_post_info/', main_views.set_post_info.as_view(), name='set_post_info'),
    path('delete_post_info/', main_views.delete_post_info.as_view(), name='delete_post_info'),
    path('get_chat_response/', main_views.get_chat_response.as_view(), name='get_chat_response'),
]
