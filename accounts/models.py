from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
    
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    Profile_name = models.CharField(max_length=255, unique=True,blank=True , null=True)
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_photo', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, unique=True,null=True,blank=True)
    

    Role_choices = (
        ('freelancer', 'freelancer'),
        ('client', 'client'),
    )
    role = models.CharField(max_length=20, choices=Role_choices, null=True, blank=True)
    
    profile_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    
    
    
    
    
class Otp(models.Model):
    user_id = models.ForeignKey( User , on_delete=models.CASCADE, related_name='otps')
    otp = models.IntegerField()
    

    
        

    
    
    
    
    