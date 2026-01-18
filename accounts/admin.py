from django.contrib import admin
from .models import User, Otp,Rating

# Register your models here.

admin.site.register(User)
admin.site.register(Otp)
admin.site.register(Rating)
