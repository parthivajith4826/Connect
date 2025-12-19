from django.shortcuts import render,redirect
from .forms import SignupForm, Reset_passwordForm
from django.contrib.auth import authenticate
from .models import User, Otp
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login




from django.core.mail import send_mail
from django.conf import settings
import secrets

@never_cache
# Create your views here.
def landing_page(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    else :
        return render(request,'landing_page.html')
    
    # #temp aytt vechathane
    # return render(request,'landing_page.html')


@never_cache
#Procedure 1
def register(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
        
        
        
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            verification_link = request.build_absolute_uri(f"/verify_email/{user.email_verification_token}/")
            
            email  = form.cleaned_data.get('email')
            send_mail(
            subject="Verify your email",
            message=f"Click this link to verify your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
            request.session['register_email'] = email #It is used to resent the email , also it is used in the adpaters.
            user = form.save()
            
            return render(request, "accounts/email_sent.html",{'email':email}) 
            
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


@never_cache
def resent_email(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    
    
    
    
    
    email = request.session.get('register_email')
    
    # #alteration
    # del request.session['register_email']
    
    user = User.objects.filter(email = email).first()
    
    if user :
    
        token = user.email_verification_token
        if token:
            verification_link = request.build_absolute_uri(f"/verify_email/{token}/")

            
            send_mail(
                    subject="Verify your email",
                    message=f"Click this link to verify your email: {verification_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )

            return render(request, "accounts/email_sent.html",{'email':email})  
        else :
            return render(request, "accounts/email_sent.html",{'email':email,'error':'The Email is verified, You can sign in to Your account.'})  

    else :
        return render(request,'accounts/error/verification_error2.html')
    
    


@never_cache
#procedure 2, this page is come from the link that is got the user from thei email.
def verify_email(request,token):
    
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home') 
        else :
            return redirect('client:home')
    
    
    
    
    
    
    user = User.objects.filter(email_verification_token = token).first()
    
    if user:
        user.is_verified = True
        user.email_verification_token = None
        user.save()
        request.session['email'] = user.email # this session is created for to use in the upcoming procedures
        # 'email' session created after sign in, actually in this step user is saved in the database , thats why say that after sign in.
        return render(request,'accounts/select_role.html')
    else :
        return render(request,'accounts/error/verification_error.html')
    
        
 
@never_cache   
#procedure 3 
def role(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    
    
    
    
    
    
    if request.method == 'POST':
        email = request.session.get('email')
        # email_social = request.user.email
        
        # #alteration
        # del request.session['email']
        
        #This is the normal case of role selection when user sign up with email and passowrd
        if email:
            user = User.objects.filter(email = email).first()
            role = request.POST.get('role')
            user.role = role
            user.save()
            
            
            request.session['user_email'] = email
            
            
            if user.role == "freelancer":
                return redirect('freelancer:home')
            else :
                return redirect('client:home')
        
        #This is the else case , it is mean that normal email is not existed, that means user is trying to sign up with social account , that means 
        # trying to sign up with google.
        #in this case in order to get the email , that is used for social sign up we are using request.user.email.
        else:
            if request.user.email :
                # return redirect('accounts:role')
                #request.user.email is email that is used when sign up with google
                user = User.objects.filter(email = request.user.email).first()
                # del request.session['email_social']
                role = request.POST.get('role')
                user.role = role
                user.save()
                print("socail role saved")
                request.session['user_email'] = request.user.email
                
                if user.role == "freelancer":
                    return redirect('freelancer:home')
                else :
                    return redirect('client:home')
            
            
    else :
        #Why these conditions is here
        #because after sign in or sign up with social acocount redirected to this page , role selection.
        #at that time the method will GET
        #So this lines are writterned for users who already sign up successfully by using social account.
        #if they are sign up once successfylly, there should be a role freelancer or client, so they are redirected to the respective page ,
        #if they are not chose role during sign up , or they are on their sign up process it will go to the above ines of logic for a fresher user
        email_social = request.user.email
        user = User.objects.filter(email = email_social).first()
        
        # request.session['user_email'] = request.user.email
        
        
        if user.role:
            if user.role == "freelancer":
                return redirect('freelancer:home')
            else :
                return redirect('client:home')
        return render(request,'accounts/select_role.html')




@never_cache
def signin(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
        
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request,email = email, password = password)
        if user :
            # if user.
            if user.is_verified :  
                
                request.session['user_email'] = email
                login(request,user)
                
                print(request.session.get('user_email'))  
                if user.role == "freelancer":
                        return redirect('freelancer:home')
                else :
                    return redirect('client:home')   
            else :
                return render(request,'accounts/login.html',{"error":"Email is not verified.You can verify email by simply clicking the link that we sent on your Email"})
        else :
            return render(request,'accounts/login.html',{"error":"Invalid email or password.<br>Signed up with Google? Use Google to log in.<br>Account not verified earlier? Please sign up again."})
    else :
        return render(request,'accounts/login.html')


@never_cache
def request_otp(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    
    
    
    
    
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email = email).first()
        request.session['otp_email'] = email
        
        if user :
            
            if request.session.get('otp_sent'):
                return render(request,'accounts/forgot_password.html',{'message':'Check Your Email,Otp Has been sent.'}) 
            
            else :
            
                otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
                
                send_mail(
                subject="OTP",
                message=otp,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
                Otp.objects.create(user_id = user,otp = otp)
                request.session['otp_sent'] = True
                return redirect('accounts:otp')
        else :
            return render(request,'accounts/forgot_password.html',{'error':'Invalide Email'})
    return render(request,'accounts/forgot_password.html')
    
  
@never_cache  
def resent_otp(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    
    
    
    
    email = request.session.get('otp_email')
    user = User.objects.filter(email = email).first()
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
                
           
    send_mail(
    subject="OTP",
    message=otp,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[email],
)
    temp = Otp.objects.filter(user_id = user)
    temp.delete()
    Otp.objects.create(user_id = user,otp = otp)
    return redirect('accounts:otp')
    

@never_cache
def otp(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    
    
    
    
    
    request.session['otp_sent'] = False
    if request.method == 'POST':
        email = request.session.get('otp_email')
        otp = request.POST.get('otp1'),request.POST.get('otp2'),request.POST.get('otp3'),request.POST.get('otp4'),request.POST.get('otp5'),request.POST.get('otp6') 
        user = User.objects.get(email = email)
        
        for i in user.otps.all():
            if tuple(str(i.otp)) == otp:
                return redirect('accounts:reset_password')
            else :
                return render(request,'accounts/otp.html',{'error':'Invalid Otp'})
        
    return render(request,'accounts/otp.html')



@never_cache
def reset_password(request):
    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    
    
    
    
    
    
    if request.method == 'POST':
        form = Reset_passwordForm(request.POST)
        if form.is_valid():
            email = request.session.get('otp_email')
            user = User.objects.get(email = email)
            #Set_password() is used for hashing the password as like in the usercreation form
            user.set_password(form.cleaned_data.get("password1"))
            user.save()
            return redirect('accounts:signin')
        else :
            return render(request,'accounts/reset_password.html',{'form':form})
    
    form = Reset_passwordForm()
    return render(request,'accounts/reset_password.html',{'form':form})
                                    
                                    


@never_cache
def social_email_conflict(request):
    

    if request.session.get('user_email'):
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        if user.role == "freelancer":
            return redirect('freelancer:home')
        else :
            return redirect('client:home')
    
    
    
    
    return render(request, "account/social_email_conflict.html")