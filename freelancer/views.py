from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from client.models import User
from .models import Freelancer_Profile,Gig,GigImages
from management.models import SubscriptionPack,UserSubscription,SubscriptionTransaction
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
from datetime import timedelta
from django.utils import timezone

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



def subscriptions(request):
    subscriptions = SubscriptionPack.objects.all()[1:]
    freeplan = SubscriptionPack.objects.all()[0]
    
    return render(request,"freelancer/subscriptions.html",{"subscriptions":subscriptions,"freeplan":freeplan})

import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect


stripe.api_key = settings.STRIPE_SECRET_KEY



def subscribe_start(request, slug):
    
    #for to give in subscriptions.html (subscriptions,freeplan,pack)
    subscriptions = SubscriptionPack.objects.all()[1:]
    freeplan = SubscriptionPack.objects.all()[0]
    pack = get_object_or_404(SubscriptionPack, slug=slug, is_active=True)
    
    user1 = request.user
    usersubscription = UserSubscription.objects.filter(user = user1).first()
    
    if usersubscription :
        if usersubscription.subscription_pack.plantype.name == "Free" or not usersubscription.is_active :
            if not usersubscription.is_active:
                usersubscription.delete()
            # ✅ Create PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(pack.price * 100),
                currency="inr",
                automatic_payment_methods={
                "enabled": True,},
                metadata={
                    "user_id": request.user.id,
                    "subscription_pack_id": pack.id,
                    "purpose" : "subscription",
                }
            )

            return render(request, "freelancer/subscribe_pay.html", {
                "client_secret": intent.client_secret,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
                "pack": pack,
                "success_url": request.build_absolute_uri(
                        "/freelancer/subscription-success"
                    ),
            })
        
        else :
            return render(request,"freelancer/subscriptions.html",{"error":"You already have a Subscription,Wait until for an expiry for next subscription","subscriptions":subscriptions,"freeplan":freeplan})
    
    else :
        print("usersubscription illa")
        intent = stripe.PaymentIntent.create(
                amount=int(pack.price * 100),
                currency="inr",
                automatic_payment_methods={
                "enabled": True,},
                metadata={
                    "user_id": request.user.id,
                    "subscription_pack_id": pack.id,
                    "purpose" : "subscription",
                }
            )

        return render(request, "freelancer/subscribe_pay.html", {
            "client_secret": intent.client_secret,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "pack": pack,
            "success_url": request.build_absolute_uri(
                    "/freelancer/subscription-success"
                ),
        })
        
        
        
    
    
    # return HttpResponse("Subscriptions")



from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from decimal import Decimal
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook_subscription(request):
    print("webhook reached")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_SUBSCRIPTION_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_type = event["type"]
    print(f"event type = {event_type}")
    
    intent = event["data"]["object"]
    metadata = intent.get("metadata", {})
    print(metadata)

    print(f"Purpose = {metadata.get("purpose")}")
    # 🔐 Validate this webhook is for subscriptions
    if metadata.get("purpose") != "subscription":
        return HttpResponse(status=200)
    print(f"Purpose = {metadata.get("purpose")}")

    user_id = metadata.get("user_id")
    print(f"userid = {user_id}")
    pack_id = metadata.get("subscription_pack_id")
    print(f"pack id = {pack_id}")

    if not user_id or not pack_id:
        return HttpResponse(status=200)

    # 🔐 Validate user & pack
    try:
        user = User.objects.get(id=user_id)
        pack = SubscriptionPack.objects.get(id=pack_id, is_active=True)
        print(f"pack = {pack}")
    except (User.DoesNotExist, SubscriptionPack.DoesNotExist):
        return HttpResponse(status=200)

    amount = Decimal(intent["amount"]) / Decimal("100")

    # =====================================================
    # ✅ PAYMENT SUCCEEDED → CREATE SUBSCRIPTION
    # =====================================================
    if event_type == "payment_intent.succeeded":
        print("success ayittund")

        

        start_date = timezone.now()
        end_date = start_date + timedelta(days=pack.duration_days)

        subscription, _ = UserSubscription.objects.update_or_create(
            user=user,
            defaults={
                "subscription_pack": pack,
                "start_date": start_date,
                "end_date": end_date,
            }
        )
        print("User subscription updated")
        SubscriptionTransaction.objects.get_or_create(
            stripe_payment_intent_id=intent["id"],
            defaults={
                "user": user,
                "user_subscription": subscription,
                "amount": amount,
                "payment_status": "succeeded",
            }
        )
        print("transactions also updated")

    # =====================================================
    # ❌ PAYMENT FAILED → RECORD FAILURE
    # =====================================================
    elif event_type == "payment_intent.payment_failed":

        SubscriptionTransaction.objects.get_or_create(
            stripe_payment_intent_id=intent["id"],
            defaults={
                "user": user,
                "user_subscription": None,
                "amount": amount,
                "payment_status": "failed",
            }
        )

    # =====================================================
    # 🚫 PAYMENT CANCELED → RECORD CANCELLATION
    # =====================================================
    elif event_type == "payment_intent.canceled":

        SubscriptionTransaction.objects.get_or_create(
            stripe_payment_intent_id=intent["id"],
            defaults={
                "user": user,
                "user_subscription": None,
                "amount": amount,
                "payment_status": "canceled",
            }
        )

    return HttpResponse(status=200)

def subscription_success(request):
    return render(request,"freelancer/subscription_success.html")