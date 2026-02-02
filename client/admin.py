from django.contrib import admin

from .models import (Card, Card_images, Categories, Location, Wallet,
                     WalletTransactions)

# Register your models here.
admin.site.register(Location)
admin.site.register(Categories)
admin.site.register(Card)
admin.site.register(Card_images)
admin.site.register(Wallet)
admin.site.register(WalletTransactions)
