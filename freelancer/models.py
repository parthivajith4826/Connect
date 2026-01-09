from django.db import models
from client.models import User,Categories
from autoslug import AutoSlugField
# Create your models here.

class Freelancer_Profile(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255,unique=True,blank=False,null=False)
    T_user_name = models.CharField(max_length=255,unique=True,blank=False,null=False)
    
class Gig(models.Model):
    title = models.CharField(max_length=255)
    freelancer_id = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = AutoSlugField( populate_from ='title', unique = True,blank = True)
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name="categories")
    is_blocked = models.BooleanField(default=False)
    portfolio = models.CharField(max_length=255)
    price_max = models.IntegerField(null=False)
    price_min = models.IntegerField(null=False)
    skills = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class GigImages(models.Model):
    gig_id = models.ForeignKey(Gig,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="gig_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
    