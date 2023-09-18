import datetime
from authorization.apps import send_mail
from django.shortcuts import render
from django.http import request
from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.backends import ModelBackend, get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import response, decorators, permissions, status, authentication
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from authorization.seralizers import MyTokenObtainPairSerializer
import json
import random
from tripo_main_interface.models import Users
# Create your views here.

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class verification(APIView):  # send verification code
    def get(self, request):
        if 'email' in request.GET:
            email = request.GET['email']
            if cache.get(email):
                code, time = cache.get(email)
                now = timezone.now()
                if (now - time) <= datetime.timedelta(minutes=1):   # at list 1 min interval between two request
                    return HttpResponse(status=403)
            code = self.generate_code()
            cache.set(email, (code, timezone.now()), timeout=300)
            self.send(email, code)
            return HttpResponse(status=200)
        return HttpResponse(status=500)

    def send(self, email, code):
        # do something
        content = "Your have requested verification code of Tripo, your code is \n" +  \
                  "<h2>" + str(code) + "</h2>\n" + \
                  "This code can be used to register and reset password, <b> DO NOT DISTRIBUTE </b> to others. <br>" + \
                  "<right> Tripo Team </right>"
        send_mail(email, 'Tripo Verification Code', content)

    def generate_code(self):
        code = random.randint(0, 9999)
        code = "%04d" % code
        return code


class register(APIView):
    def post(self, request):
        user_info = json.loads(request.body)
        email = user_info.get('email')
        code = user_info.get('code')
        username = user_info.get('username')
        password = user_info.get('password')
        if cache.get(email) is None or code != cache.get(email)[0]:     # email verification failed
            return HttpResponse(status=403)
        cache.set(email, None)
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            user = None
        if user is not None:    # email used
            return HttpResponse(status=301)
        Users.objects.create_user(username=username, password=password, email=email)
        return HttpResponse(status=200)

class reset(APIView):
    def post(self, request):
        info = json.loads(request.body)
        email = info.get('email')
        password = info.get('password')
        code = info.get('code')
        if cache.get(email) is None or code != cache.get(email)[0]:     # email verification failed
            return HttpResponse(status=403)
        cache.set(email, None)
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return HttpResponse(status=404)
        user.set_password(password)
        user.save()
        return HttpResponse(status=200)


class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(email=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None
