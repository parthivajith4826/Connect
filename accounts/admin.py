from django.contrib import admin

from .models import Otp, Rating, User

admin.site.register(User)
admin.site.register(Otp)
admin.site.register(Rating)
