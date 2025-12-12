from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout


# Create your views here.

@never_cache
def home(request):
    if not request.session.get('user_email'):
        return redirect('accounts:landing_page')
    
    return render(request,'freelancer/home.html')



def signout(request):
    request.session.flush()
    
    logout(request)
    
    return redirect('accounts:landing_page')
    