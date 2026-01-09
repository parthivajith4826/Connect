from django.db import models
from accounts.models import User
from autoslug import AutoSlugField

# Create your models here.

class Location(models.Model):
    user_id = models.ForeignKey( User , on_delete=models.CASCADE, related_name='location')
    location_name = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    
    
class Categories(models.Model):
    name = models.CharField(max_length=255,null=False)
    is_blocked = models.BooleanField(default=False)
    slug =AutoSlugField( populate_from ='name',blank=True)
    
    def __str__(self):
        return self.name
    
class Card(models.Model):
    title = models.CharField(max_length=255,null=False)
    slug =AutoSlugField( populate_from ='title', unique = True)
    category_id = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name="category")
    client_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="client")
    skills_required = models.CharField(max_length=500,null=False)
    description = models.TextField() #This is for ckeditor page
    min_budget = models.IntegerField(null=False)
    max_budget = models.IntegerField(null=False)
    time_line = models.CharField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    

    
class Card_images(models.Model):
    card_id = models.ForeignKey(Card,on_delete=models.CASCADE,related_name="image")
    image = models.ImageField(upload_to="card_images/")
    
    
class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_blocked = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    

        
class WalletTransactions(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_type = models.CharField(max_length=20 , choices=(("credit", "Credit"), ("debit", "Debit")))
    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20)  # success / failed / pending
    created_at = models.DateTimeField(auto_now_add=True)