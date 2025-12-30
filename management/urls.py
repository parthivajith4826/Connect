from django.urls import path
from . import views


apps = 'control_panel'
urlpatterns = [
    path('',views.home,name = 'control_panel'),
]
