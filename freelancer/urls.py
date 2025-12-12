from django.urls import path
from . import views

app_name = 'freelancer'
urlpatterns = [
    path('',views.home,name = 'home'),
    path('signout/',views.signout,name = 'signout'),
]
