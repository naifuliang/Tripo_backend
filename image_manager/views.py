from django.shortcuts import render
from django.http import HttpResponse, request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from image_manager.models import image_item
from tripo_main_interface.models import Posts
# Create your views here.

# class image_item(models.Model):
#     id = models.AutoField(primary_key=True, verbose_name='id')  # primary key
#     post = models.ForeignKey('tripo_main_interface.Posts', on_delete=models.CASCADE, related_name='images')
#     file_name = models.TextField(default='unnamed image')   # file name
#     time = models.TimeField(default=timezone.now)  # upload time
#     image = models.ImageField(upload_to='post_img') # posted images
#     def __unicode__(self):  # __str__ on Python 3
#         return (self.id, self.image)

#     def __str__(self):
#         return str(self.file_name)

# add a new img to the database
class push_img(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        img_info = request.POST                                                
        post_id = img_info.get('post_id')
        
        # try to get the post by post_id
        try:                                            # if the post exists
            post = Posts.objects.get(post_id=post_id)   # get the post
        except Posts.DoesNotExist:                      # if not exists
            return HttpResponse(status=404)             # 404 not found
        
        file_name = img_info.get('file_name')
        time = img_info.get('time')
        image = request.FILES.get('image')
        img = image_item(post=post, file_name=file_name, time=time, image=image)  # create a new image_item object
        img.save()                                                                # save the new img
        return HttpResponse(status=200)                   
    
# delete a existing img from the database
class delete_img(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request):
        img_info = request.POST     
        img_id = img_info.get('img_id')
        
        # try to get the post by post_id
        try:                                            # if the img exists
            img = image_item.objects.get(id=img_id)     # get the img
            img.delete()                                # save the new img
            return HttpResponse(status=200)             # 200 OK
        except image_item.DoesNotExist:                 # if not exists
            return HttpResponse(status=404)             # 404 not found
        
  