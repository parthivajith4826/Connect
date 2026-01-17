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
    
    path('add-fund',views.add_fund,name = 'add_fund'),
    path("withdraw/", views.withdraw, name="withdraw"),
    
    
    path("manage-proposals/<slug:slug>/", views.manage_proposals, name="manage_proposals"),
    path("gig-details/<slug:gig_slug>/<slug:card_slug>/", views.gig_details, name="gig_details"),
    path("connection/", views.connections, name="connections"),
    
    
    #temp
    # path("hello/", views.hello_page, name="hello_page"),
    # path("qr/", views.qr_code, name="qr_code"),
    
    

]
