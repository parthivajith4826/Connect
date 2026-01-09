from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from client.models import User
from .models import Freelancer_Profile,Gig,GigImages
from client.models import Categories
from.forms import ProfileForm,ContactForm,CreategigForm


# Create your views here.

@never_cache
def home(request):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page') 
    # if not request.session.get('user_email'):
    #     return redirect('accounts:landing_page')
    # if not request.session.get('user_email'):
    #     # email = request.session.get('user_email')
    #     # user = User.objects.get(email=email)
    #     # if user.role == "freelancer":
    #     #     return redirect('freelancer:home')
    #     # else :
    #     #     return redirect('client:home')
    #     return redirect('accounts:landing_page')
    else :
    
        if user.is_authenticated:
            if not user.profile_completed:
                return render(request,'freelancer/errors/profile_error.html')
            else :
                gigs = Gig.objects.filter(freelancer_id = user) 
        
        
            return render(request,'freelancer/home.html',{'gigs':gigs})
        else :
            return redirect('accounts:signin')
    
    
    
    
@never_cache
def profile(request):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page') 
    
    
    user = request.user
    print(user)
    profile = Freelancer_Profile.objects.filter(user_id = user).first()
    print(profile)
    if request.method == 'POST':
        form1 = ProfileForm(request.POST,request.FILES,instance=request.user)
        form2 = ContactForm(request.POST , instance=profile)
        if form1.is_valid() and form2.is_valid() :
            user.profile_completed = True
            form1.save()
            contact = form2.save(commit=False)
            contact.user_id = request.user
            contact.save()  
        else :
            return render(request,'freelancer/profile.html',{'form1':form1,'form2':form2})
        
        return redirect('freelancer:home')
        
    else :
        form1 = ProfileForm(instance = user)
        form2 = ContactForm(instance = profile)
    
    return render(request,'freelancer/profile.html',{'form1':form1,'form2':form2,'profile':profile})




# def gigs(request):
    
#     user = request.user
#     print(user)
#     gigs = Gig.objects.filter(freelancer_id = user)

#     # gigs = Gig.objects.all()
#     # gig_images = GigImages.objects.filter(gig_id__in= gigs)
#     return render(request,'freelancer/gig_list.html',{"gigs":gigs})


@never_cache
def add_gig(request):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page')
    
    
    categories = Categories.objects.all()
    if request.method == 'POST':
        form =CreategigForm(request.POST,request.FILES)
        images = request.FILES.getlist("images")

        
        is_form_valid = form.is_valid()

        
        if images:
            if len(images) > 3:
                form.add_error(None, "You can upload a maximum of 3 images only.")
                is_form_valid = False

            allowed_types = ["image/jpeg", "image/png"]
            for img in images:
                if img.content_type not in allowed_types:
                    form.add_error(
                        None, "Only JPG and PNG images are allowed."
                    )
                    is_form_valid = False


        
        if is_form_valid:
            
            # category = request.POST.get("categories")
            # category = category.split(',') if category else []
            # category_ids = list(map(int,category))
            
            gig = form.save(commit=False)
            gig.freelancer_id = request.user
            
            gig.save()
            
            # gig = Gig.objects.get(id = gig.id)
            # gig.categories.set(category_ids)

            # gig = Gig.objects.get(id = gig.id)
            # print(gig)
            for img in images:
                GigImages.objects.create(
                    gig_id=gig,
                    image=img
                )

            return redirect("freelancer:home")
            
        else :
            
            
            return render(request,'freelancer/add_gig.html',{'categories':categories,'form':form})
    
    # category = request.POST.get("categories")
    # category = category.split(',') if category else []
    # category_ids = list(map(int,category))
    # categories = Categories.objects.filter(id__in=category_ids)
    # print(categories)
   
    # print(request.POST)
    # print(request.POST.getlist('categories'))
    # categories = request.POST.getlist('categories').split(",")
    form = CreategigForm()
    return render(request,'freelancer/add_gig.html',{'form':form,'categories':categories})


@never_cache
def view_gig(request,slug):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page')
    
    gig = Gig.objects.get(slug = slug)
    skills = gig.skills
    skills = skills.split(",")
    return render(request,'freelancer/view_gig.html',{'gig':gig,'skills':skills})




@never_cache
def edit_gig(request,slug):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page')
    
    
    gig = Gig.objects.get(slug=slug)
    images_db = gig.images.all()                                                                                                                                                                                                                                                                                                                        
    categories = Categories.objects.filter(is_blocked=False)

    if request.method == "POST":
        
        form = CreategigForm(request.POST,instance=gig)
        images = request.FILES.getlist("images")

        deleted_image_ids = request.POST.get('deleted_image_ids')
        if deleted_image_ids:
            list =deleted_image_ids.split(",")
            for i in list:
                images_db.get(id=int(i)).delete()



        is_form_valid = form.is_valid()



        if images:
            if images_db.count() + len(images) > 3:
                form.add_error(None, "You can upload a maximum of 3 images only.")
                is_form_valid = False

            allowed_types = ["image/jpeg", "image/png"]
            for img in images:
                if img.content_type not in allowed_types:
                    form.add_error(
                        None, "Only JPG and PNG images are allowed."
                    )
                    is_form_valid = False

        
        if is_form_valid:
            print(is_form_valid)

            # category = request.POST.get("categories")
            # category = category.split(',') if category else []
            # category_ids = list(map(int,category))

            gig = form.save(commit=False)
            gig.freelancer_id = request.user
            gig.save()

            # gig = Gig.objects.get(id = gig.id)
            # gig.categories.set(category_ids)

            # gig = Gig.objects.get(id = gig.id)
            # print(gig)
            for img in images:
                GigImages.objects.create(
                    gig_id=gig,
                    image=img
                )

            return redirect("freelancer:home")
        else :
            print("valid alla")

            return render(request,"freelancer/add_gig.html",{"form": form,"categories": categories,"Gig":gig,"images":images_db})


    form = CreategigForm(instance = gig)
    return render(request,"freelancer/add_gig.html",{"form": form,"categories": categories,"gig":gig,"images":images_db})

@never_cache
def close_gig(request,slug):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page')
    
    
    gig = Gig.objects.get(slug=slug)
    gig.delete()
    return redirect("freelancer:home")


@never_cache
def signout(request):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page')
    
    
    request.session.flush()
    
    
    logout(request)
    
    return redirect('accounts:landing_page')




import uuid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt
def quill_image_upload(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        print(f"image -- {image}")
        filename = f"quill/{uuid.uuid4().hex}_{image.name}"
        path = default_storage.save(filename, ContentFile(image.read()))
        image_url = default_storage.url(path)

        return JsonResponse({
            "success": True,
            "url": image_url
        })

    return JsonResponse({"success": False}, status=400)

