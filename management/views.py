from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from accounts.models import User
from freelancer.models import Gig,Freelancer_Profile,GigImages
from client.models import Card,Categories,WalletTransactions,Wallet,Card_images
from django.http import Http404
from .forms import CategoryForm,SubscriptionForm,PlanTypeForm,EditSubscriptionForm
from .models import Plantype,SubscriptionPack
from django.http import JsonResponse

# Create your views here.

def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")      
        password = request.POST.get("password")      
        user = authenticate(request,email = email, password = password)
        if user.is_superuser:
            return redirect("control_panel:home")
    else :
        return render(request,"management/signin.html")
    
    
def home(request):
    users = User.objects.all()
    user_count = users.count()
    
    freelancer_count = User.objects.filter(role = "freelancer").count()
    gig = Gig.objects.all()
    card = Card.objects.all()
    category = Categories.objects.all()
    category_count = category.count()
    gig_count  = gig.count()
    client_count = User.objects.filter(role = "client").count()
    card_count = card.count()
    txn = WalletTransactions.objects.all()
    pending_txn = WalletTransactions.objects.filter(status = "pending")
    pending_txn_count = pending_txn.count()
    
    
    
    
    return render(request,"management/dashboard.html",{"user_count":user_count,"freelancer_count":freelancer_count,
                "client_count":client_count,"gig_count":gig_count,"card_count":card_count,"category_count":category_count,
                "pending_txn_count":pending_txn_count})
    
    

def pending_transactions(request):
    pending_txn = WalletTransactions.objects.filter(status = "pending")
    return render(request,"management/pending-transactions.html",{"pending_txn":pending_txn})

def freelancers(request):
    freelancers = User.objects.filter(role = "freelancer")
    return render(request,"management/freelancers.html",{"freelancers":freelancers})

def freelancer_block(request,profile_name):
    try:
        user = User.objects.filter(Profile_name = profile_name).first()
    except User.DoesNotExist:
        raise Http404("User not found")

    user.is_active = False
    user.save()
    return redirect("control_panel:freelancers" )

def freelancer_unblock(request,profile_name):
    try:
        user = User.objects.filter(Profile_name = profile_name).first()
    except Gig.DoesNotExist:
        raise Http404("User not found")

    user.is_active = True
    user.save()
    return redirect("control_panel:freelancers" )
        
def freelancer_view_profile(request,profile_name):
    user = User.objects.filter(Profile_name = profile_name).first()
    profile = Freelancer_Profile.objects.get(user_id = user)
    gigs = Gig.objects.filter(freelancer_id = user)
    gig_count = gigs.count()
    return render(request,"management/freelancer-detail.html",{"user":user,"profile":profile,"count":gig_count})


def freelancer_gig_list(request,profile_name):
    user = User.objects.filter(Profile_name = profile_name).first()
    gigs = Gig.objects.filter(freelancer_id = user)
    return render(request,"management/freelancer-gigs-list.html",{"user":user,"gigs":gigs})

def total_gigs(request):
    gigs = Gig.objects.all()
    return render(request,"management/all-gigs.html",{"gigs":gigs})


def gig_block(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = True
    gig.save()
    return redirect("control_panel:freelancer_gig_list",gig.freelancer_id.Profile_name )

def gig_block2(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = True
    gig.save()
    return redirect("control_panel:view_gig",gig.slug )

def gig_block3(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = True
    gig.save()
    return redirect("control_panel:all_gig_list")

def gig_unblock(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = False
    gig.save()
    return redirect("control_panel:freelancer_gig_list",gig.freelancer_id.Profile_name )

def gig_unblock2(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = False
    gig.save()
    return redirect("control_panel:view_gig",gig.slug )

def gig_unblock3(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = False
    gig.save()
    return redirect("control_panel:all_gig_list")


def view_gig(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")
    gig_images = GigImages.objects.filter(gig_id=gig)
    skills = gig.skills
    skills = skills.split(",")
    return render(request,"management/gig-detail.html",{"gig":gig,"gig_images":gig_images,"skills":skills})


def categories(request):
    categories = Categories.objects.all()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("control_panel:categories")
    else:
        form = CategoryForm()

    return render(request,"management/categories.html",{"categories": categories,"form": form,})


def category_block(request,slug):
    category = Categories.objects.get(slug = slug)
    category.is_blocked = True
    category.save()
    return redirect("control_panel:categories")

def category_unblock(request,slug):
    category = Categories.objects.get(slug = slug)
    category.is_blocked = False
    category.save()
    return redirect("control_panel:categories")

def category_delete(request,slug):
    category = Categories.objects.get(slug = slug)
    category.delete()
    return redirect("control_panel:categories")



def clients(request):
    clients = User.objects.filter(role = "client")
    return render(request,"management/clients/clients.html",{"clients":clients})

def client_block(request,profile_name):
    try:
        client = User.objects.filter(Profile_name = profile_name).first()
    except User.DoesNotExist:
        raise Http404("User not found")

    client.is_active = False
    client.save()
    return redirect("control_panel:clients")

def client_unblock(request,profile_name):
    try:
        client = User.objects.filter(Profile_name = profile_name).first()
    except User.DoesNotExist:
        raise Http404("User not found")

    client.is_active = True
    client.save()
    return redirect("control_panel:clients")




def client_view_profile(request,profile_name):
    client = User.objects.filter(Profile_name = profile_name).first()
    wallet = Wallet.objects.filter(user = client).first()
    txns = WalletTransactions.objects.filter(wallet = wallet)
    debit = 0
    credit = 0
    for txn in txns:
        if txn.transaction_type == "credit":
            credit += txn.amount
        else :
            debit += txn.amount
    cards = Card.objects.filter(client_id = client)
    cards_count = cards.count()
    return render(request,"management/clients/client-detail.html",{"client":client,"wallet":wallet,"credit":credit,"debit":debit,"cards_count":cards_count})


def client_wallet_transactions(request,profile_name):
    client = User.objects.get(Profile_name = profile_name)
    wallet = Wallet.objects.get(user = client)
    txns = WalletTransactions.objects.filter(wallet = wallet)
    return render(request,"management/clients/client-wallet-transactions.html",{"client":client,"txns":txns})

def txn_update(request,id):
    if request.method == "POST":
        status = request.POST.get("status")
        txn = WalletTransactions.objects.get(id = id)
        txn.status = status
        txn.save()
        return redirect("control_panel:client_wallet_transactions",txn.wallet.user.Profile_name)

    return render(request,"management/clients/client-wallet-transactions.html",{"client":None,"txns":WalletTransactions.objects.none()}) 
    
def freeze_wallet(request,id):
    wallet = Wallet.objects.get(id = id)
    wallet.is_blocked = True
    wallet.save()
    return redirect("control_panel:client_profile",wallet.user.Profile_name )
       
def unfreeze_wallet(request,id):
    wallet = Wallet.objects.get(id = id)
    wallet.is_blocked = False
    wallet.save()
    return redirect("control_panel:client_profile",wallet.user.Profile_name )

def client_cards_list(request,profile_name):
    
    user = User.objects.filter(Profile_name = profile_name).first()
    cards = Card.objects.filter(client_id = user)
    return render(request,"management/clients/client-cards-list.html",{"user":user,"cards":cards})
    
    
def card_block(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = True
    card.save()
    return redirect("control_panel:client_cards_list",card.client_id.Profile_name)

def card_block2(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = True
    card.save()
    return redirect("control_panel:view_card",card.slug)

def card_block3(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = True
    card.save()
    return redirect("control_panel:all_cards_list")

def card_unblock(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = False
    card.save()
    return redirect("control_panel:client_cards_list",card.client_id.Profile_name )

def card_unblock2(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = False
    card.save()
    return redirect("control_panel:view_card",card.slug )

def card_unblock3(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = False
    card.save()
    return redirect("control_panel:all_cards_list")





def view_card(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")
    card_images = Card_images.objects.filter(card_id=card)
    skills = card.skills_required
    skills = skills.split(",")
    return render(request,"management/clients/card-detail.html",{"card":card,"card_images":card_images,"skills":skills})


def total_cards(request):
    cards = Card.objects.all()
    return render(request,"management/clients/all-cards.html",{"cards":cards})


def logout(request):
    request.session.flush()
    return redirect("accounts:landing_page")

def subscriptions(request):
    subscriptions = SubscriptionPack.objects.all()
    return render(request,"management/subscription_list.html",{"subscriptions":subscriptions})

def create_subscriptions(request):
    plantype = Plantype.objects.filter(is_active = True)
    form = SubscriptionForm()
    plantype_form = PlanTypeForm()
    
    if request.method == "POST": 
        
        if request.POST.get("form_type") == "subscription":
            
            print(request.POST)
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("control_panel:subscriptions")
            
        # elif request.POST.get("form_type") == "plantype":
        #     print("plan type")
        #     plantype_form = PlanTypeForm(request.POST)
        #     if plantype_form.is_valid():
        #         print(plantype_form.id)
        #         plantype_form.save()
        #         plantype_form = PlanTypeForm()
        #     else :
        #         print(plantype_form.errors)
        
        elif request.POST.get("form_type") == "plantype":
            plantype_form = PlanTypeForm(request.POST)

            if plantype_form.is_valid():
                plantype = plantype_form.save()
                print(plantype.id)
                return JsonResponse({
                    "success": True,
                    "id": plantype.id,
                    "name": plantype.name,
                })

            return JsonResponse({
                "success": False,
                "errors": plantype_form.errors,
            }, status=400)

    return render(request,"management/create_subscription.html",{"form":form,"plantype_form":plantype_form,"plantype":plantype})


def edit_subscription(request,slug):
    subscriptionpack = SubscriptionPack.objects.filter(slug = slug).first()
    plantype = Plantype.objects.all()
    form = EditSubscriptionForm(instance = subscriptionpack)
    if request.method == "POST":
        form = EditSubscriptionForm(request.POST,instance = subscriptionpack)
        if form.is_valid():
            print("valid")
            form.save()  
    
    
    return render(request,"management/edit_subscription.html",{"form":form,"plantype":plantype})
    

