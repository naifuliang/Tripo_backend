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
from .utils import get_access_token
import requests
# Create your views here.

class get_user_info(APIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
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
    
    
# get a existing post from the database
class get_post_info(APIView):
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
        
        # return the post information from database
        res = {
            "post_id": post.post_id,
            "username": post.user.username,
            "email": post.user.email,
            "avatar": post.user.avatar.url if post.user.avatar else None,
            "title": post.title,
            "content": post.content, 
            "time":post.time,
            "location":post.location
        }
        return JsonResponse(res)

# update a existing post in the database
class set_post_info(APIView):
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
        if post_id is not None:                        
            post.post_id = post_id
        if user is not None:
            post.user = user
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
    
# add a new post to the database
class push_post_info(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user                                        # get post info from request body
        post_info = request.POST                                   
        title = post_info.get('title')
        content = post_info.get('content')
        location = post_info.get('location')
        time = post_info.get('time')
                                
        post = Posts(user=user,\
                                title=title,\
                                    content=content,\
                                        time=time,\
                                            location=location)     # create a new post
        post.save()                                            # save the new post
        return HttpResponse(status=200)                            # 200 OK
    

# delete a existing post from the database
class delete_post_info(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request):
        # get post info and user info from request body
        user = request.user
        post_info = request.POST                    
        post_id = post_info.get('post_id')
        post = Posts.objects.filter(post_id=post_id,user=user) 
        
        if post.exists():                            # if the post already exists
            post.delete()                            # delete the post
            return HttpResponse(status=200)          # return HTTP 200
        else:                                        # if not exists
           return HttpResponse(status=404)           # return HTTP 404
        

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
            
