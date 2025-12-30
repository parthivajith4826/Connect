from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from accounts.models import User
from .models import Location,Card_images,Card,Categories,Wallet,WalletTransactions
from .forms import ProfileForm,LocationForm,CreatecardForm

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
    
def add_fund(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        print(request.user)
    
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

        
    return render(request,'client/add_funds.html')
   

def wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = WalletTransactions.objects.filter(wallet=wallet).order_by("-created_at")

    return render(request, "client/wallet.html", {
        "wallet": wallet,
        "transactions": transactions
    })
    
    
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from decimal import Decimal

@csrf_exempt
def stripe_webhook(request):
    print("Webhhok etheettend")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET
    )
    print(event["type"])

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        user_id = intent["metadata"]["user_id"]
        # amount = intent["amount"] / 100
        
        amount = Decimal(intent["amount"]) / Decimal("100")

        wallet = Wallet.objects.get(user_id=user_id)
        wallet.balance += amount
        wallet.save()

        WalletTransactions.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type="credit",
            stripe_payment_intent=intent["id"],
            status="success"
        )

    # return HttpResponse(status=200)
    return redirect('client:wallet')
