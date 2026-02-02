from django.contrib import admin
from .models import Location,Categories,Card,Card_images,Wallet,WalletTransactions

# Register your models here.
admin.site.register(Location)
admin.site.register(Categories)
admin.site.register(Card)
admin.site.register(Card_images)
admin.site.register(Wallet)
admin.site.register(WalletTransactions)


