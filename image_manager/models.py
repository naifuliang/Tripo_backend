from django.db import models
from django.utils import timezone
# Create your models here.

class image_item(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')  # primary key
    post = models.ForeignKey('tripo_main_interface.Posts', on_delete=models.CASCADE, related_name='images')
    # file_name = models.TextField(default='unnamed image')   # file name
    time = models.TimeField(default=timezone.now)  # upload time
    image = models.ImageField(upload_to='post_img')     # posted images
    def __unicode__(self):  # __str__ on Python 3
        return (self.id, self.image)

    # def __str__(self):
    #     return str(self.file_name)