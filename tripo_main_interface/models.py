from django.db import models

import image_manager.models


# Create your models here.

class Users(models.Model):
    uid = models.AutoField(primary_key=True)    # primary key, uid, unique identifier in back end
    username = models.TextField(default='unnamed user')     # username
    password = models.TextField(default='')     # password, ought to be encrypted in front end
    email = models.TextField(default='')    # email, format should be checked before stored
    avatar = models.ImageField(upload_to='avatars', default=None)   # user avatar, use supported format
    # posts, foreign key related name

class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)    # primary key
    user = models.ForeignKey('Users', on_delete=True, related_name='posts')   # user who posts
    title = models.TextField(default='unnamed post')    # title of the post
    content = models.TextField(default='')  # content of the post
    time = models.TimeField()   # post time, local time
    location = models.TextField(default='')     # location, generated & resolved in front end
    # images, foreign key related name
