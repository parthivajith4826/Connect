from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from client.models import User
from .models import Freelancer_Profile
from.forms import ProfileForm,ContactForm


# Create your views here.

@never_cache
def home(request): 
    # if not request.session.get('user_email'):
    #     return redirect('accounts:landing_page')
    if not request.session.get('user_email'):
        # email = request.session.get('user_email')
        # user = User.objects.get(email=email)
        # if user.role == "freelancer":
        #     return redirect('freelancer:home')
        # else :
        #     return redirect('client:home')
        return redirect('accounts:landing_page')
    else :
    
    
        return render(request,'freelancer/home.html')

def profile(request):
    user = request.user
    profile = Freelancer_Profile.objects.filter(user_id = user).first()
    print(profile)
    if request.method == 'POST':
        form1 = ProfileForm(request.POST,request.FILES,instance=request.user)
        form2 = ContactForm(request.POST , instance=profile)
        if form1.is_valid() and form2.is_valid() :
            form1.save()
            contact = form2.save(commit=False)
            contact.user_id = request.user
            contact.save()  
        else :
            return render(request,'freelancer/profile.html',{'form1':form1,'form2':form2})
        
        return redirect('freelancer:profile')
        
    else :
        form1 = ProfileForm(instance = user)
        form2 = ContactForm(instance = profile)
    
    return render(request,'freelancer/profile.html',{'form1':form1,'form2':form2,'profile':profile})


def signout(request):
    request.session.flush()
    
    
    logout(request)
    
    return redirect('accounts:landing_page')
    