from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('',views.landing_page,name = 'landing_page'),
    path('register/',views.register,name = 'register'),
    path('signin/',views.signin,name = 'signin'),
    path('request-otp/',views.request_otp,name = 'request_otp'),
    path('otp/',views.otp,name = 'otp'),
    path('resent-otp/',views.resent_otp,name = 'resent_otp'),
    path('reset-password/',views.reset_password,name = 'reset_password'),
    path('verify_email/<uuid:token>/',views.verify_email,name = 'verify_email'),
    path('role/',views.role,name = 'role'),
    
    path("login-method-error/", views.social_email_conflict, name="social_email_conflict"),
    path("resend_email/",views.resent_email,name = 'resent_email'),

]
