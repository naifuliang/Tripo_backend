import json
from django.shortcuts import render
from django.http import request
from django.core import cache
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import HttpResponse, JsonResponse
from tripo_main_interface.models import Users, Posts
from django.contrib.auth.models import AnonymousUser

# Create your views here.

class get_user_info(APIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        if 'uid' in request.GET:
            uid = request.GET['uid']
            try:
                user = Users.objects.get(id=uid)
            except Users.DoesNotExist:
                user = None
        else:
            user = request.user
        res = {
            "uid": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar.url if user.avatar else None
        }
        return JsonResponse(res)

class set_user_info(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        user_info = json.loads(request.body)
        username = user_info.get('username')
        email = user_info.get('email')
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        user.save()
        return HttpResponse(status=200)