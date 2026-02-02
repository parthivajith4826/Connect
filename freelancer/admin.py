from django.contrib import admin

from .models import Connections, Freelancer_Profile, Gig, GigImages

# Register your models here.
admin.site.register(Freelancer_Profile)
admin.site.register(Gig)
admin.site.register(GigImages)
admin.site.register(Connections)
