from django.contrib import admin

from .models import Plantype,SubscriptionPack,UserSubscription,SubscriptionTransaction

admin.site.register(Plantype)
admin.site.register(SubscriptionPack)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionTransaction)


