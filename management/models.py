from django.db import models
from autoslug import AutoSlugField

# Create your models here.
class Plantype(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default = True)
    
    def __str__(self):
        return self.name
    
class SubscriptionPack(models.Model):
    title = models.CharField(max_length=100)
    slug =AutoSlugField(populate_from ='title')
    plantype = models.ForeignKey(Plantype,on_delete=models.CASCADE,related_name="packs")
    max_gigs = models.PositiveIntegerField()
    max_images_per_gig = models.PositiveBigIntegerField()
    connection_limit = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

    
