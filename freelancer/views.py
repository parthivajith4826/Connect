from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from client.models import User
from .models import Freelancer_Profile,Gig,GigImages,Connections
from management.models import SubscriptionPack,UserSubscription,SubscriptionTransaction,Total_pack
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
    
        if not user.profile_completed:
            return render(request,'freelancer/errors/profile_error.html')
        else :
            gigs = Gig.objects.filter(freelancer_id = user) 
            connections_count = Connections.objects.all().count()
            connections_accepted = Connections.objects.filter(status = 'accepted').count()
            connections_pending = Connections.objects.filter(status = 'pending').count()
            connections_rejected = Connections.objects.filter(status = 'rejected').count()
            
    
        return render(request,'freelancer/home.html',{'gigs':gigs,'connections_count':connections_count,'connections_accepted':connections_accepted,'connections_pending':connections_pending,'connections_rejected':connections_rejected})

    
    
    
    
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


from django.urls import reverse
@never_cache
def add_gig(request):
    user = request.user
    # print(user)
    if not user.is_authenticated: 
       return redirect('accounts:landing_page')
   
    usersubscription = UserSubscription.objects.filter(user = user,is_active = True)
    total_pack = Total_pack.objects.filter(user = user).first()
    
    #check the user have a subscription or not
    if usersubscription :
    #if they have, can make the gigs for themselves

        if not total_pack.gig_count == 0 : #checking the gig_count,gig creation is only possible if it is greater than 0
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
                        
                    #After the gig creation decrease the number of gig_count,gig_image_count,connection_limit
                    gig_count = total_pack.gig_count 
                    if not gig_count == 0 :
                        gig_count = gig_count - 1
                        total_pack.gig_count = gig_count
                        total_pack.save()

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
    
        else :
            gigs = Gig.objects.all()
            upgrade_url = reverse("freelancer:subscriptions")
            error = f'You’ve reached your gig limit.<a href="{upgrade_url}">Please upgrade your subscription</a> to create more gigs.'
            return render(request,"freelancer/home.html",{"gigs":gigs,"error":error})            
            
    else :
        gigs = Gig.objects.all()
        error = "User doesn't have an active Subscription"
        return render(request,"freelancer/home.html",{"gigs":gigs,"error":error})


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

            return render(request,"freelancer/edit_gig.html",{"form": form,"categories": categories,"Gig":gig,"images":images_db})


    form = CreategigForm(instance = gig)
    return render(request,"freelancer/edit_gig.html",{"form": form,"categories": categories,"gig":gig,"images":images_db})

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
    
    #for give in subscriptions.html (subscriptions,freeplan,pack)
    # subscriptions = SubscriptionPack.objects.all()[1:]
    # freeplan = SubscriptionPack.objects.all()[0]
    pack = get_object_or_404(SubscriptionPack, slug=slug, is_active=True)
                                                  
    
    
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
                "/freelancer/subscription/result/"
            ),
    })
    
    
        




from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from decimal import Decimal
import stripe
from django.db import transaction
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook_subscription(request):
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
    
    intent = event["data"]["object"]
    metadata = intent.get("metadata", {})

    # Validate this webhook is for subscriptions
    if metadata.get("purpose") != "subscription":
        return HttpResponse(status=200)

    user_id = metadata.get("user_id")
    pack_id = metadata.get("subscription_pack_id")

    if not user_id or not pack_id:
        return HttpResponse(status=200)

    # Validate user & pack
    try:
        user = User.objects.get(id=user_id)
        pack = SubscriptionPack.objects.get(id=pack_id, is_active=True)
        print(f"pack = {pack.connection_limit}")
    except (User.DoesNotExist, SubscriptionPack.DoesNotExist):
        return HttpResponse(status=200)

    amount = Decimal(intent["amount"]) / Decimal("100")

    # payment Successful
    if event_type == "payment_intent.succeeded":
        
        with transaction.atomic():

            start_date = timezone.now()
            end_date = start_date + timedelta(days=pack.duration_days)

            subscription= UserSubscription.objects.create(
                user=user,
                subscription_pack=pack,
                start_date=start_date,
                end_date=end_date
            )
            total_pack = Total_pack.objects.select_for_update().get(user=user)
            gig_count = total_pack.gig_count + pack.max_gigs
            connection_limit = total_pack.connection_limit + pack.connection_limit
            
            total_pack, _ = Total_pack.objects.update_or_create(
                user=user,
                defaults={
                    "gig_count": gig_count,
                    "connection_limit": connection_limit})
            
            
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

    #Payment Failed
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

    #Payment Cancelled logiv
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





def subscription_result(request):
    intent_id = request.GET.get("payment_intent")

    if not intent_id:
        return redirect("freelancer:subscriptions")

    tx = SubscriptionTransaction.objects.filter(
        stripe_payment_intent_id=intent_id
    ).first()

    if not tx:
        # webhook has NOT arrived yet
        return render(request, "freelancer/subscription_pending.html")

    if tx.payment_status == "succeeded":
        return render(request, "freelancer/subscription_success.html")

    if tx.payment_status == "failed":
        return render(request, "freelancer/subscription_failed.html")

    if tx.payment_status == "canceled":
        return render(request, "freelancer/subscription_canceled.html")

    return render(request, "freelancer/subscription_pending.html")






from client.models import Card,Categories
def find_work(request):
    print(request.GET)
    categories = Categories.objects.all()
    search_keyword = request.GET.get("q")
    category = request.GET.get("category")
    skills = request.GET.get("skills")
    minimum_price = request.GET.get("min_price")
    maximum_price = request.GET.get("max_price")
    timeline = request.GET.get("timeline")
    
    
    cards = Card.objects.none()
    if search_keyword :
        cards = Card.objects.filter(title__icontains = search_keyword, is_blocked = False )
        # cards = cards.filter(is_active = )
    if category :
        cards = cards.filter(category_id = category )
    if skills :
        cards = cards.filter(skills_required__icontains = skills)
    
    if minimum_price is not None and maximum_price is not None:
        cards = cards.filter(
            min_budget__gte = minimum_price,
            max_budget__lte=maximum_price
        )
    
    if timeline :
        cards = cards.filter(time_line__icontains = timeline)
        
    if request.GET.get("newest"):
        cards = cards.order_by("-created_at")


    return render(request,"freelancer/find_work.html",{"cards":cards,"categories":categories})



def card_details(request,slug):
    card = get_object_or_404(Card,slug = slug)
    skill_list = card.skills_required.split(",")
    return render(request,"freelancer/card_details.html",{"card":card,"skill_list":skill_list})


def show_gigs(request,card_slug=None):
    card = get_object_or_404(Card,slug = card_slug)
    gigs = Gig.objects.filter(freelancer_id = request.user)
    gig_count = gigs.count()
    usersubscription = UserSubscription.objects.filter(user = request.user,is_active = True)
    if not usersubscription :
        messages.error(request, "No active subscriptions. Unable to establish a connection.")
        return redirect('freelancer:show_gigs',card.slug)
    
    total_pack = Total_pack.objects.get(user=request.user)
    if total_pack.connection_limit == 0:
        messages.error(request, "Connection limit reached (0). No new connections can be established.")
    return render(request,"freelancer/show-gigs.html",{"gigs":gigs,"gig_count":gig_count,"card":card,"total_pack":total_pack})

def show_gig_details(request,slug):
    gig = get_object_or_404(Gig,slug = slug)
    skill_list = gig.skills.split(",")
    print(gig.images.all())
    for image in gig.images.all():
        print(image)
    return render(request,"freelancer/show_gig_details.html",{"gig":gig,"skill_list":skill_list})





from django.contrib import messages
from django.core.exceptions import PermissionDenied
def create_connection(request, card_slug):
    #this is created for , when creating connection object
    card = get_object_or_404(Card, slug=card_slug)
    client_user = card.client_id

    gig_slug = request.POST.get("gig_slug")
    gig = get_object_or_404(Gig,slug=gig_slug,freelancer_id=request.user)
    
    
    try :
        total_pack = Total_pack.objects.get(user=request.user) 
    except Total_pack.DoesNotExist:
        raise PermissionDenied("No Active Subsciption")
        #this will auto open the 403.html
        
        
    with transaction.atomic():
        connection, created = Connections.objects.get_or_create(
            user = request.user,
            client_user = client_user,
            card=card,
            gig=gig
        )
        
        if created :
            connection_limit = total_pack.connection_limit - 1
                
            total_pack.connection_limit = connection_limit
            total_pack.save()
        
    
    if not created:
        # Already exists → respect status
        if connection.status == "pending":
            gigs = Gig.objects.all()
            gig_count = gigs.count()
            messages.warning(request, "Connection request already pending.")
            return render(request,"freelancer/show-gigs.html",{"gigs":gigs,"gig_count":gig_count,"card":card})
        elif connection.status == "accepted":
            gigs = Gig.objects.all()
            gig_count = gigs.count()
            messages.info(request, "You are already connected.")
            return render(request,"freelancer/show-gigs.html",{"gigs":gigs,"gig_count":gig_count,"card":card})
        elif connection.status == "rejected":
            gigs = Gig.objects.all()
            gig_count = gigs.count()
            messages.error(request, "This request was rejected earlier.")
            return render(request,"freelancer/show-gigs.html",{"gigs":gigs,"gig_count":gig_count,"card":card})

    else:
        messages.success(request, "Connection request sent successfully.")


    return redirect('freelancer:work_details', card.slug)

def subscription_details(request):
    subscriptions = UserSubscription.objects.filter(user = request.user).order_by("-created_at")
    total_pack = get_object_or_404(Total_pack,user = request.user)
    return render(request,'freelancer/subscription_status.html',{"subscriptions":subscriptions,"total_pack":total_pack})


def my_connections(request):
    connections = Connections.objects.filter(user = request.user)
    connections_count = connections.count()
    return render(request,"freelancer/my_connections.html",{"connections":connections,"connections_count":connections_count})


def gig_preview(request,slug):
    gig = Gig.objects.filter(slug = slug).first()
    skills = gig.skills
    skills = skills.split(",")    
    return render(request,"freelancer/gig_preview.html",{"gig":gig,"skills":skills})