from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from accounts.models import User
from .models import Location,Card_images,Card,Categories
from .forms import ProfileForm,LocationForm,CreatecardForm

@never_cache
# Create your views here.
def home(request):
    user = request.user
    print(user.is_authenticated)
    if user.is_authenticated:
        if not user.profile_completed:
            return render(request,'client/errors/profile_error.html')
        else :
            card = Card.objects.filter(client_id = user).prefetch_related('image')
            count = Card.objects.count()
            # card = Card.obejcts.all()
            return render(request,'client/home.html',{'count':count,'card':card})
    else :
        return redirect('accounts:signin')


@never_cache
def signout(request):
    request.session.flush()
    
    logout(request)
    
    return redirect('accounts:landing_page')
    
    
@never_cache
def profile(request):
    
    user = request.user
    if request.method == 'POST':
        form1 = ProfileForm(request.POST,request.FILES,instance=user)
        form2 = LocationForm(request.POST)
        # print(request.POST)
        print(form1.is_valid(),form2.is_valid())
        if form1.is_valid() and form2.is_valid():  
            # user.profile_photo = None
            user.save()
            user.profile_completed = True
            
            form1.save()
            location_form = form2.save(commit=False)
            # print(form2,location_form)
            location_form.user_id = user
            location_form.save()
            
            
            return redirect('client:profile')
        else:
            return render(request,'client/profile.html',{'form1':form1,'form2':form2})
    
    else :  
        form1 = ProfileForm(instance=user)
        location = Location.objects.filter(user_id = user).order_by('-id').first()
        
        
        if location :
            form2 = LocationForm(instance = location)
        else :
            form2 = LocationForm()
        return render(request,'client/profile.html',{'user':user,'form1':form1,'form2':form2})

@never_cache
def wallet(request):
    return render(request,'client/wallet.html')

@never_cache
def create_card(request):
    categories = Categories.objects.filter(is_blocked=False)
    print(request.POST)

    if request.method == "POST":
        form = CreatecardForm(request.POST)
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
            card = form.save(commit=False)
            card.client_id = request.user
            card.save()

            
            for img in images:
                Card_images.objects.create(
                    card_id=card,
                    image=img
                )

            return redirect("client:home")

        
        return render(
            request,
            "client/create_card.html",{"form": form,"categories": categories,}
        )

   
    form = CreatecardForm()
    return render(
        request,"client/create_card.html",{"form": form,"categories": categories,}
    )



@never_cache
def view_card(request,slug):
    
    card = Card.objects.filter(slug = slug).first()
    if card :
        images = Card_images.objects.filter(card_id = card)
        skill_list = card.skills_required.split(",")
        return render(request,'client/view.html',{'card':card,'images':images,'skill_list':skill_list})
    else :
        return render(request,'accounts/home.html',{'error':'IIssue with the Card'})
    
    
@never_cache   
def edit_card(request,slug):
    card = Card.objects.get(slug=slug)
    images_db = card.image.all()
    categories = Categories.objects.filter(is_blocked=False)
    
    if request.method == "POST":
        # print(request.POST)
        # print(request.FILES)
        form = CreatecardForm(request.POST,instance=card)
        images = request.FILES.getlist("images")
        
        deleted_image_ids = request.POST.get('deleted_image_ids')
        # print(deleted_image_ids)
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
            card = form.save(commit=False)
            card.client_id = request.user
            card.save()

            
            for img in images:
                Card_images.objects.create(
                    card_id=card,
                    image=img
                )

            return redirect("client:home")

        
        return render(request,"client/create_card.html",{"form": form,"categories": categories,"card":card,"images":images_db})

    
    form = CreatecardForm()
    return render(request,"client/create_card.html",{"form": form,"categories": categories,"card":card,"images":images_db})
    

@never_cache
def close_card(request,slug):
    card = Card.objects.get(slug=slug)
    card.delete()
    return redirect("client:home")
    
    
    
        
   

