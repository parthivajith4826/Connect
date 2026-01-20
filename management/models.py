from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from datetime import timedelta
from accounts.models import User

# Create your models here.
class Plantype(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default = True)
    
    def __str__(self):
        return f"{self.id} - {self.name}" 
    
class SubscriptionPack(models.Model):
    title = models.CharField(max_length=100)
    slug =AutoSlugField(populate_from ='title')
    plantype = models.ForeignKey(Plantype,on_delete=models.CASCADE,related_name="packs")
    max_gigs = models.PositiveIntegerField()
    max_images_per_gig = models.PositiveBigIntegerField(default=0)
    connection_limit = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_most_popular = models.BooleanField(default=False)
    # is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} - {self.title} {self.slug}" 
    

    
class UserSubscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="subscription")

    subscription_pack = models.ForeignKey(SubscriptionPack,on_delete=models.PROTECT,related_name="user_subscriptions")
    created_at = models.DateTimeField(auto_now_add=True)
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True,blank=True)

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(
                days=self.subscription_pack.duration_days
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.subscription_pack.title}"
    



class Total_pack(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="total_pack")
    gig_count = models.IntegerField(default = 0)
    connection_limit = models.IntegerField(default = 0)
    
    




class SubscriptionTransaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="subscription_transactions")

    user_subscription = models.ForeignKey(UserSubscription,on_delete=models.CASCADE,related_name="transactions")

    stripe_payment_intent_id = models.CharField(max_length=255,unique=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(
        max_length=50,
        choices=[
            ("succeeded", "Succeeded"),
            ("failed", "Failed"),
            ("canceled", "Canceled"),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    


class Pricing(models.Model):
    card_creation_price = models.DecimalField(max_digits=10,decimal_places=2,default = 0.00)

    connection_price = models.DecimalField(max_digits=10,decimal_places=2,default = 0.00)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Card: ₹{self.card_creation_price} | Connection: ₹{self.connection_price}"

