from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from accounts.models import User,Rating
from .models import Location,Card_images,Card,Categories,Wallet,WalletTransactions
from .forms import ProfileForm,LocationForm,CreatecardForm
from management.models import Pricing
from django.db import transaction




import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

@never_cache
# Create your views here.
def home(request):
    user = request.user
    print(user.is_authenticated)
    if user.is_authenticated:
        if not user.profile_completed:
            return render(request,'client/errors/profile_error.html')
        else :
            card = Card.objects.filter(client_id = user).prefetch_related('image').order_by("-created_at")
            count = Card.objects.count()
            wallet = Wallet.objects.filter(user = user).first()
            connection = Connections.objects.filter(client_user = request.user)
            pending_count = connection.filter(status = "pending").count()
            success_count = connection.filter(status = "accepted").count()
            print(success_count)
            rejected_count = connection.filter(status = "rejected").count()
            return render(request,'client/home.html',{'count':count,'card':card,"wallet":wallet,'pending_count':pending_count,'success_count':success_count,'rejected_count':rejected_count})
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

# @never_cache
# def wallet(request):
#     return render(request,'client/wallet.html')

@never_cache
def create_card(request):
    categories = Categories.objects.filter(is_blocked=False)

    wallet = get_object_or_404(Wallet,user = request.user)
    pricing = Pricing.objects.get(id = 1)
    
    if request.method == "POST":
        
        with transaction.atomic():
        
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
                
                wallet.balance -= pricing.card_creation_price 
                wallet.save()
                WalletTransactions.objects.create(wallet = wallet,amount = pricing.card_creation_price,transaction_type = "debit",status = "success" )
                
                return redirect("client:home")

            
            # return render(
            #     request,
            #     "client/create_card.html",{"form": form,"categories": categories,}
            # )
    
    error = None
    if pricing.card_creation_price > wallet.balance :
        error = "Error: Insufficient funds. Unable to create the required card."
    form = CreatecardForm()
    return render(
        request,"client/create_card.html",{"form": form,"categories": categories,"pricing":pricing,"wallet":wallet,"error":error}
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
                Card_images.objects.create(card_id=card,image=img)

            return redirect("client:home")

        
        return render(request,"client/create_card.html",{"form": form,"categories": categories,"card":card,"images":images_db})

    
    form = CreatecardForm(instance = card)
    return render(request,"client/create_card.html",{"form": form,"categories": categories,"card":card,"images":images_db})
    

@never_cache
def close_card(request,slug):
    card = Card.objects.get(slug=slug)
    card.delete()
    return redirect("client:home")
    
def add_fund(request):
    if request.method == 'POST':
        wallet = Wallet.objects.filter(user = request.user).first()
        if not wallet.is_blocked:
            amount = request.POST.get('amount')
            
            if not amount or int(amount) <= 0:
                return render(request,"client/add_funds.html",{"error":"Enter a valid amount"})
            
                    # create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(amount) * 100,
                currency="inr",
                metadata={
                    "user_id": request.user.id,
                    "purpose": "wallet_topup"
                }
            )
            
            return render(
                request,
                "client/confirm_payment.html",
                {
                    "client_secret": intent.client_secret,
                    "amount": amount,
                    "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
                }
            )

        else :
            return render(request,'client/add_funds.html',{"error":"Wallet is disabled"})
        
    return render(request,'client/add_funds.html')
   

def wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = WalletTransactions.objects.filter(
        wallet=wallet
    ).order_by("-created_at")[:4]

    message = None
    message_type = None  # success / error / warning

    pi = request.GET.get("pi")
    print(pi)
    if pi:
        txn = WalletTransactions.objects.filter(
            stripe_payment_intent=pi
        ).order_by("-created_at").first()

        if txn:
            if txn.status == "success":
                message = "Payment successful. Wallet credited."
                message_type = "success"

            elif txn.status == "failed":
                message = "Payment failed. No amount was deducted."
                message_type = "error"

            elif txn.status == "canceled":
                message = "Payment was canceled."
                message_type = "warning"

            elif txn.status == "refunded":
                message = "Payment was refunded. Amount removed from wallet."
                message_type = "warning"

    return render(
        request,
        "client/wallet.html",
        {
            "wallet": wallet,
            "transactions": transactions,
            "message": message,
            "message_type": message_type,
        },
    )
    
    



from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from decimal import Decimal
import stripe

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WALLET_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_type = event["type"]
    data_object = event["data"]["object"]
    metadata = data_object.get("metadata", {})
    
    if metadata.get("purpose") != "wallet_topup":
        return HttpResponse(status=200)
   

    if event_type.startswith("payment_intent"):
        intent = data_object

        user_id = intent["metadata"].get("user_id")
        if not user_id:
            return HttpResponse(status=200)

        amount = Decimal(intent["amount"]) / Decimal("100")
        wallet, _ = Wallet.objects.get_or_create(user_id=user_id)

        
        if event_type == "payment_intent.succeeded":
            txn, created = WalletTransactions.objects.get_or_create(
                stripe_payment_intent=intent["id"],
                defaults={
                    "wallet": wallet,
                    "amount": amount,
                    "transaction_type": "credit",
                    "status": "success",
                }
            )

            if created:
                wallet.balance += amount
                wallet.save()

       
        elif event_type == "payment_intent.payment_failed":
            WalletTransactions.objects.get_or_create(
                stripe_payment_intent=intent["id"],
                defaults={
                    "wallet": wallet,
                    "amount": amount,
                    "transaction_type": "credit",
                    "status": "failed",
                }
            )

        
        elif event_type == "payment_intent.canceled":
            WalletTransactions.objects.get_or_create(
                stripe_payment_intent=intent["id"],
                defaults={
                    "wallet": wallet,
                    "amount": amount,
                    "transaction_type": "credit",
                    "status": "canceled",
                }
            )


    elif event_type == "charge.refunded":
        charge = data_object
        intent_id = charge["payment_intent"]
        amount = Decimal(charge["amount_refunded"]) / Decimal("100")

        txn = WalletTransactions.objects.filter(
            stripe_payment_intent=intent_id,
            status="success"
        ).first()

        if txn:
            wallet = txn.wallet
            wallet.balance -= amount
            wallet.save()

            WalletTransactions.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type="debit",
                stripe_payment_intent=intent_id,
                status="refunded",
            )

    
    return HttpResponse(status=200)


from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def withdraw(request):
    wallet = Wallet.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
        except:
            return render(request, "client/withdraw.html", {
                "error": "Invalid amount"
            })

        if amount <= 0:
            return render(request, "client/withdraw.html", {
                "error": "Amount must be greater than zero"
            })

        if amount > wallet.balance:
            return render(request, "client/withdraw.html", {
                "error": "Insufficient wallet balance"
            })

       
        wallet.balance -= amount
        wallet.save()

        
        WalletTransactions.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type="debit",
            status="pending",
        )

        return redirect("client:wallet")

    return render(request, "client/withdraw.html")


import uuid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt
def quill_image_upload(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]

        base_name = sanitize_filename(image.name)
        ext = os.path.splitext(image.name)[1]

        filename = f"quill/{base_name}_{uuid.uuid4().hex[:8]}{ext}"

        path = default_storage.save(filename, ContentFile(image.read()))
        image_url = default_storage.url(path)

        return JsonResponse({
            "success": True,
            "url": image_url
        })

    return JsonResponse({"success": False}, status=400)

import uuid
import os
import re

def sanitize_filename(name):
    name = os.path.splitext(name)[0]          # remove extension
    print(name)
    name = re.sub(r'[^a-zA-Z]+', '_', name)    # letters only
    return name.strip('_').lower()

from freelancer.models import Connections,Gig
from django.shortcuts import get_object_or_404
def manage_proposals(request,slug):
    card = get_object_or_404(Card,slug = slug)
    connections = Connections.objects.filter(card = card).exclude(status = "rejected")
    return render(request,"client/manage_proposals.html",{"connections":connections})


def gig_details(request,gig_slug,card_slug):
    gig = get_object_or_404(Gig,slug = gig_slug)
    skills = gig.skills
    skills = skills.split(",")
    card = get_object_or_404(Card,slug = card_slug )
    connection = get_object_or_404(Connections,gig = gig,card = card)
    rating = Rating.objects.filter(reviewer = request.user,gig = gig).first()
    pricing = Pricing.objects.get(id = 1)
    wallet = get_object_or_404(Wallet,user = request.user)
    error = None
    if pricing.connection_price > wallet.balance :
        error = "Error: Insufficient funds. Unable to connect."
    return render(request,"client/view_proposal_gig.html",{"gig":gig,"skills":skills,"card":card,"connection":connection,"rating":rating,"pricing":pricing,"error":error,"wallet":wallet})


def connections(request):
    if request.method == "POST":
        action = request.POST.get("action")
        card_slug = request.POST.get("card_slug")
        gig_slug = request.POST.get("gig_slug")

        if action == "accept":
            gig = get_object_or_404(Gig, slug=gig_slug)
            card = get_object_or_404(Card, slug=card_slug)

            connection = Connections.objects.filter(
                gig=gig,
                card=card
            ).first()
            
            connection.status = "accepted"
            connection.save()
            messages.success(request, "🎉 Connection established!  You’re now connected, and contact details are ready to view.")
            return redirect("client:gig_details",gig.slug,card.slug)


        elif action == "reject":
            gig = get_object_or_404(Gig, slug=gig_slug)
            card = get_object_or_404(Card, slug=card_slug)

            connection = Connections.objects.filter(
                gig=gig,
                card=card
            ).first()
            
            connection.status = "rejected"
            connection.save()
    return redirect("client:gig_details",gig.slug,card.slug)


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

def review(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    rating = request.POST.get("rating")
    card_slug = request.POST.get("card_slug")
    gig_slug = request.POST.get("gig_slug")

    redirect_url = (request.META.get("HTTP_REFERER") or "client/" )

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            messages.error(request, "Invalid rating")
            return redirect(redirect_url)

        card = get_object_or_404(Card, slug=card_slug)
        gig = get_object_or_404(Gig, slug=gig_slug)

        rating_old = Rating.objects.filter(reviewer=request.user,gig=gig).first()

        if not rating_old:
            Rating.objects.create(
                reviewer=request.user,
                freelancer=gig.freelancer_id,
                gig=gig,
                stars=rating
            )
            messages.success(request, "Your rating was submitted successfully ⭐")
        else:
            messages.warning(request, "You already rated this gig")

    except (TypeError, ValueError):
        messages.error(request, "Invalid rating")
        return redirect(redirect_url)

    return redirect(redirect_url)


    
    





# def hello_page(request):
#     return render(request, "freelancer/hello.html")

# import qrcode
# from io import BytesIO
# from django.http import HttpResponse
# from django.urls import reverse

# def qr_code(request):
#     path = reverse("client:hello_page")  # resolves to /client/hello/
#     url = request.build_absolute_uri(path)
#     img = qrcode.make(url)

#     buffer = BytesIO()
#     img.save(buffer, format="PNG")

#     return HttpResponse(buffer.getvalue(), content_type="image/png")



