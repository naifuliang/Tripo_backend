from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import image_manager.models


# Create your models here.

class Users(AbstractUser):
    id = models.AutoField(primary_key=True)    # primary key, uid, unique identifier in back end
    username = models.TextField(default='unnamed user')     # username
    password = models.TextField(default='')     # password, ought to be encrypted in front end
    email = models.TextField(default='')    # email, format should be checked before stored
    avatar = models.ImageField(upload_to='avatars', default='../media/static/default_avatar.jpg')   # user avatar, use supported format
    # posts, foreign key related name

class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)    # primary key
    user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='posts')   # user who posts
    title = models.TextField(default='unnamed post')    # title of the post
    content = models.TextField(default='')  # content of the post
    time = models.TimeField(default=timezone.now)   # post time, local time
    location = models.TextField(default='')     # location, generated & resolved in front end
    # images, foreign key related name
