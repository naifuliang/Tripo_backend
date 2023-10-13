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
from django.db.models import Q
from tripo_main_interface.models import Users, Posts
from image_manager.models import image_item
from django.contrib.auth.models import AnonymousUser
from .utils import get_access_token
from django.utils import timezone
import requests
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
                # user = None
                return HttpResponse(status=404)
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
        # email = user_info.get('email')
        if username is not None:
            user.username = username
        # if email is not None:
        #     user.email = email
        user.save()
        return HttpResponse(status=200)

class upload_user_avatar(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        avatar = request.FILES['avatar']
        user.avatar = avatar
        user.save()
        return HttpResponse(status=200)



class publish_post(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user                                        # get post info from request body
        title = request.POST['title']
        content = request.POST['content']
        location = request.POST['location']
        files = request.FILES.getlist('images')
        # for image in files:
        post = Posts.objects.create(user=user, title=title, content=content, time=timezone.now(), location=location)
        for image in files:
            image_item.objects.create(post=post, image=image)
        res = {
            "post_id": post.post_id
        }
        return JsonResponse(res)


class get_post(APIView):
    def get(self, request):
        # get the post in the database 
        if 'post_id' in request.GET:
            post_id = request.GET['post_id']
            try:
                post = Posts.objects.get(post_id=post_id)
            except Posts.DoesNotExist:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=500)

        images = image_item.objects.filter(post=post)
        image_urls = [image.image.url for image in images]
        # return the post information from database
        res = {
            "post_id": post.post_id,
            "username": post.user.username,
            "email": post.user.email,
            "avatar": post.user.avatar.url if post.user.avatar else None,
            "title": post.title,
            "content": post.content, 
            "time": post.time,
            "location": post.location,
            "images": image_urls
        }
        return JsonResponse(res)

# update an existing post in the database
class modify_post(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        # get post's info and user's info from request body
        user = request.user                                        
        post_info = request.POST                                   
        post_id = post_info.get('post_id')
        title = post_info.get('title')
        content = post_info.get('content')
        location = post_info.get('location')
        time = post_info.get('time')
        
        # try to get the post
        try:                                            # if the post exists
            post = Posts.objects.get(post_id=post_id)   # get the post
        except Posts.DoesNotExist:                      # if not exists
            return HttpResponse(status=404)             # 404 not found
        
        # if new information exist, update the post
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if time is not None:
            post.time = time
        if location is not None:
            post.location = location
            
        post.save()                                  # save the new post
        return HttpResponse(status=200)              # 200 OK
    

# delete an existing post from the database
class delete_post(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request):
        # get post info and user info from request body
        user = request.user
        post_id = request.GET['post_id']
        try:
            post = Posts.objects.get(post_id=post_id, user=user)
        except Posts.DoesNotExist:
            return HttpResponse(status=404)
        post.delete()
        return HttpResponse(status=200)

class post_list(APIView):
    def get(self, request):
        up, down = int(request.GET['up']), int(request.GET['down'])
        if 'uid' in request.GET:
            uid = request.GET['uid']
            if uid != 0:
                posts = Posts.objects.filter(user__id=uid).order_by('-time')[up: down]
            else:
                posts = Posts.objects.all().order_by('-time')[up: down]
        else:
            user = request.user
            posts = Posts.objects.filter(user=user).order_by('-time')[up: down]
        res = []
        for post in posts:
            images = image_item.objects.filter(post=post)
            image_urls = [image.image.url for image in images]
            post_info = {
                "post_id": post.post_id,
                "username": post.user.username,
                "email": post.user.email,
                "avatar": post.user.avatar.url if post.user.avatar else None,
                "title": post.title,
                "content": post.content,
                "time": post.time,
                "location": post.location,
                "images": image_urls
            }
            res.append(post_info)
        return JsonResponse(res, safe=False)

# get the AI LLM chat response from baidu company
class get_chat_response(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # get the chat info from request
        chat_query = request.GET.get('chat_info')   # 输入需要LLM大模型处理的介绍内容，比如某海滩某山脉的名字
        
        if chat_query is None:
            return HttpResponse(status=500)
        
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token() # get the access token from baidu company

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": "假设你是一名资深导游，请为游客们简要介绍一下{}".format(chat_query)
                }
            ]
        })
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        return JsonResponse(json.loads(response.text))
            
