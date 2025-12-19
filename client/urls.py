from django.urls import path
from .import views

app_name = 'client'
urlpatterns = [
    path('',views.home,name = 'home'),
    path('signout/',views.signout,name = 'signout'),
    path('profile/',views.profile,name = 'profile'),
    path('wallet/',views.wallet,name = 'wallet'),
    path('create-card/',views.create_card,name = 'create_card'),
    path('view-card/<slug:slug>/',views.view_card,name = 'view_card'),
    path('edit-card/<slug:slug>/',views.edit_card,name = 'edit_card'),
    path('close-card/<slug:slug>/',views.close_card,name = 'close_card'),
]
