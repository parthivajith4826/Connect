from django.contrib import admin

from .models import (Plantype, Pricing, SubscriptionPack,
                     SubscriptionTransaction, Total_pack, UserSubscription)

admin.site.register(Plantype)
admin.site.register(SubscriptionPack)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionTransaction)
admin.site.register(Total_pack)
admin.site.register(Pricing)
