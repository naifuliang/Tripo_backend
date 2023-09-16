from django.db import models

# Create your models here.

class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.TextField(default='unnamed user')
    password = models.TextField(default='')
    email = models.TextField(default='')
    avatar = models.ImageField(upload_to='avatars')