from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from accounts.models import User,Rating
from .models import Location,Card_images,Card,Categories,Wallet,WalletTransactions
from .forms import ProfileForm,LocationForm,CreatecardForm
from management.models import Pricing
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.urls import reverse_lazy
import uuid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import re
from freelancer.models import Connections,Gig
from django.contrib import messages
from django.http import HttpResponseBadRequest




@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def home(request):
    user = request.user
    if not user.profile_completed:
        return render(request,'client/errors/profile_error.html')
    
    card = Card.objects.filter(client_id = user).prefetch_related('image').order_by("-created_at")
    count = Card.objects.count()
    wallet = Wallet.objects.filter(user = user).first()
    connection = Connections.objects.filter(client_user = request.user)
    pending_count = connection.filter(status = "pending").count()
    success_count = connection.filter(status = "accepted").count()
    rejected_count = connection.filter(status = "rejected").count()
    wallet_transactions = WalletTransactions.objects.filter(wallet = wallet)
    debit = 0
    for txn in wallet_transactions :
        if txn.transaction_type == "debit" :
            debit += txn.amount
    return render(request,'client/home.html',{'count':count,'card':card,"wallet":wallet,'pending_count':pending_count,'success_count':success_count,'rejected_count':rejected_count,'debit':debit})
   

@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def signout(request):
    request.session.flush()
    logout(request)
    return redirect('accounts:landing_page')
    
    
@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def profile(request):
    
    user = request.user
    if request.method == 'POST':
        form1 = ProfileForm(request.POST,request.FILES,instance=user)
        form2 = LocationForm(request.POST)
        print(form1.is_valid(),form2.is_valid())
        if form1.is_valid() and form2.is_valid():  
            with transaction.atomic():
                user.save()
                user.profile_completed = True
                
                form1.save()
                location_form = form2.save(commit=False)
                location_form.user_id = user
                location_form.save()
                Wallet.objects.create(user = request.user)
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


@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def create_card(request):
    categories = Categories.objects.filter(is_blocked=False)

    wallet = get_object_or_404(Wallet,user = request.user)
    pricing = Pricing.objects.get(id = 1)
    
    if request.method == "POST":
        
        form = CreatecardForm(request.POST)
        images = request.FILES.getlist("images")

        
        is_form_valid = form.is_valid()
        print(is_form_valid)

        
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
            with transaction.atomic():
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

            
        return render(
            request,
            "client/create_card.html",{"form": form,"categories": categories,}
        )
    
    error = None
    if pricing.card_creation_price > wallet.balance :
        error = "Error: Insufficient funds. Unable to create the required card."
    form = CreatecardForm()
    return render(
        request,"client/create_card.html",{"form": form,"categories": categories,"pricing":pricing,"wallet":wallet,"error":error}
    )




@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def view_card(request,slug):
    
    card = Card.objects.filter(slug = slug).first()
    if card :
        images = Card_images.objects.filter(card_id = card)
        skill_list = card.skills_required.split(",")
        return render(request,'client/view.html',{'card':card,'images':images,'skill_list':skill_list})
    else :
        return render(request,'accounts/home.html',{'error':'IIssue with the Card'})
    
    

@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache  
def edit_card(request,slug):
    card = Card.objects.get(slug=slug)
    images_db = card.image.all()
    categories = Categories.objects.filter(is_blocked=False)
    
    if request.method == "POST":
        form = CreatecardForm(request.POST,instance=card)
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
            card = form.save(commit=False)
            card.client_id = request.user
            card.save()

            
            for img in images:
                Card_images.objects.create(card_id=card,image=img)

            return redirect("client:home")

        
        return render(request,"client/edit_card.html",{"form": form,"categories": categories,"card":card,"images":images_db})

    
    form = CreatecardForm(instance = card)
    return render(request,"client/edit_card.html",{"form": form,"categories": categories,"card":card,"images":images_db})
    



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def close_card(request,slug):
    card = Card.objects.get(slug=slug)
    card.delete()
    return redirect("client:home")
 
 
@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache   
def add_fund(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = Decimal(amount)
        except:
            return render(request, "client/add_funds.html", {
                "error": "Invalid amount"
            })

        if amount <= 0:
            return render(request, "client/add_funds.html", {
                "error": "Amount must be greater than zero"
            })
        
        
        if amount < 50:
            return render(request, "client/add_funds.html", {
                "error": "Minimum amount: ₹50.00"
            })

        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency="inr",
            automatic_payment_methods={"enabled": True},
            metadata={
                "purpose": "wallet_topup",
                "user_id": request.user.id,
            }
        )

        return render(request, "client/wallet_pay.html", {
            "client_secret": intent.client_secret,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "amount": amount,
            "success_url": request.build_absolute_uri(
                "/client/wallet/result/"
            ),
        })

    return render(request, "client/add_funds.html")
   


@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = WalletTransactions.objects.filter(
        wallet=wallet
    ).order_by("-created_at")[:4]

    return render(
        request,
        "client/wallet.html",
        {
            "wallet": wallet,
            "transactions": transactions,
        },
    )
    



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
@csrf_exempt
def stripe_webhook(request):
    print("Webhokk reached")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WALLET_WEBHOOK_SECRET
        )
    except:
        return HttpResponse(status=400)

    intent = event["data"]["object"]
    metadata = intent.get("metadata", {})

    if metadata.get("purpose") != "wallet_topup":
        return HttpResponse(status=200)

    user_id = metadata.get("user_id")
    if not user_id:
        return HttpResponse(status=200)

    amount = Decimal(intent["amount"]) / Decimal("100")

    with transaction.atomic():

        wallet = Wallet.objects.select_for_update().get_or_create(user_id=user_id)[0]

        if event["type"] == "payment_intent.succeeded":

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
                wallet.save(update_fields=["balance"])

        elif event["type"] == "payment_intent.payment_failed":
            WalletTransactions.objects.get_or_create(
                stripe_payment_intent=intent["id"],
                defaults={
                    "wallet": wallet,
                    "amount": amount,
                    "transaction_type": "credit",
                    "status": "failed",
                }
            )

        elif event["type"] == "payment_intent.canceled":
            WalletTransactions.objects.get_or_create(
                stripe_payment_intent=intent["id"],
                defaults={
                    "wallet": wallet,
                    "amount": amount,
                    "transaction_type": "credit",
                    "status": "canceled",
                }
            )

    return HttpResponse(status=200)



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def withdraw(request):

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

        with transaction.atomic():

            wallet = Wallet.objects.select_for_update().get(user=request.user)

            if amount > wallet.balance:
                return render(request, "client/withdraw.html", {
                    "error": "Insufficient wallet balance"
                })

            
            wallet.balance -= amount
            wallet.save(update_fields=["balance"])

            
            WalletTransactions.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type="debit",
                status="pending",
            )

        return redirect("client:wallet")

    return render(request, "client/withdraw.html")



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
def wallet_result(request):
    intent_id = request.GET.get("payment_intent")

    if not intent_id:
        return redirect("client:wallet")

    txn = WalletTransactions.objects.filter(
        stripe_payment_intent=intent_id
    ).first()

    if not txn:
        return render(request, "client/wallet_pending.html")

    if txn.status == "success":
        return render(request, "client/wallet_success.html")

    if txn.status == "failed":
        return render(request, "client/wallet_failed.html")

    if txn.status == "canceled":
        return render(request, "client/wallet_canceled.html")

    return render(request, "client/wallet_pending.html")



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache
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


@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache   
def sanitize_filename(name):
    name = os.path.splitext(name)[0]          # remove extension
    print(name)
    name = re.sub(r'[^a-zA-Z]+', '_', name)    # letters only
    return name.strip('_').lower()



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache   
def manage_proposals(request,slug):
    card = get_object_or_404(Card,slug = slug)
    connections = Connections.objects.filter(card = card).exclude(status = "rejected")
    return render(request,"client/manage_proposals.html",{"connections":connections})



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache 
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



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache 
def connections(request):
    if request.method == "POST":
        action = request.POST.get("action")
        card_slug = request.POST.get("card_slug")
        gig_slug = request.POST.get("gig_slug")
        wallet = get_object_or_404(Wallet,user = request.user)
        pricing = Pricing.objects.get(id = 1)

        if action == "accept":
            gig = get_object_or_404(Gig, slug=gig_slug)
            card = get_object_or_404(Card, slug=card_slug)

            connection = Connections.objects.filter(gig=gig,card=card).first()
            
            with transaction.atomic():
                connection.status = "accepted"
                connection.save()
                
                wallet.balance -= pricing.connection_price 
                wallet.save()
                WalletTransactions.objects.create(wallet = wallet,amount = pricing.card_creation_price,transaction_type = "debit",status = "success" )
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



@login_required(login_url=reverse_lazy('accounts:landing_page'))
@never_cache 
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


# def cancel(request):
    