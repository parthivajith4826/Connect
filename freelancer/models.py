from django.db import models
from client.models import User

# Create your models here.

class Freelancer_Profile(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255,unique=True,blank=False,null=False)
    T_user_name = models.CharField(max_length=255,unique=True,blank=False,null=False)
    