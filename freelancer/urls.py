from django.urls import path
from . import views

app_name = 'freelancer'
urlpatterns = [
    path('',views.home,name = 'home'),
    path('signout/',views.signout,name = 'signout'),
    path('profile/',views.profile,name = 'profile'),
    # path('gigs/',views.gigs,name = 'gigs'),
    path('add-gig/',views.add_gig,name = 'add_gig'),
    path('view-gig/<str:slug>',views.view_gig,name = 'view_gig'),
    path('edit-gig/<str:slug>',views.edit_gig,name = 'edit_gig'),
    path('close-gig/<str:slug>',views.close_gig,name = 'close_gig'),
    
    

]






