from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from accounts.models import User
from freelancer.models import Gig,Freelancer_Profile,GigImages,Connections
from client.models import Card,Categories,WalletTransactions,Wallet,Card_images
from django.http import Http404
from .forms import CategoryForm,SubscriptionForm,PlanTypeForm,EditSubscriptionForm,EditPlanTypeForm,PricingForm
from .models import Plantype,SubscriptionPack,Pricing,UserSubscription
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from .utilities import is_email 
from django.utils import timezone




# Create your views here.
@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('control_panel:home')
    if request.method == "POST":
        email = request.POST.get("email")      
        password = request.POST.get("password")      
        user = authenticate(request,email = email, password = password)
        if user.is_superuser:
            login(request,user)
            return redirect("control_panel:home")
    else :
        return render(request,"management/signin.html")
    

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
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
    
    
@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def pending_transactions(request):
    pending_txn = WalletTransactions.objects.filter(status = "pending")
    return render(request,"management/pending-transactions.html",{"pending_txn":pending_txn})









































@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def freelancers(request):
    freelancers = User.objects.filter(role = "freelancer")
    if request.method == "GET":
        search_keyword = request.GET.get("search")
        verification_status = request.GET.get("verified")
        subscription_status = request.GET.get("subscription")
        account_status = request.GET.get("blocked")
        date_status = request.GET.get("sort")
        if search_keyword :
            if is_email(search_keyword):
                freelancers = freelancers.filter(email__icontains = search_keyword)
            else :
                freelancers = freelancers.filter(Profile_name__icontains = search_keyword)
        if verification_status :
            if verification_status == "verified":
                freelancers = freelancers.filter(is_verified = True)
            elif verification_status == "not_verified":
                freelancers = freelancers.filter(is_verified = False)
            
        if subscription_status :
            if subscription_status == "active":
                freelancers = freelancers.filter(subscription__is_active = True).distinct()
            elif subscription_status == "inactive" :
                freelancers = freelancers.filter(subscription__is_active = False).distinct()
        if account_status :
            if account_status == "blocked":
                freelancers = freelancers.filter(is_active=False)
            elif account_status == "unblocked":
                freelancers = freelancers.filter(is_active=True)
        if date_status :
            if date_status == "newest" :
                freelancers = freelancers.order_by("-date_joined")
            elif date_status == "oldest" :
                freelancers = freelancers.order_by("date_joined")
        
    return render(request,"management/freelancers.html",{"freelancers":freelancers})









































@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def freelancer_block(request,profile_name):
    try:
        user = User.objects.filter(Profile_name = profile_name).first()
    except User.DoesNotExist:
        raise Http404("User not found")

    user.is_active = False
    user.save()
    return redirect("control_panel:freelancers" )

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def freelancer_unblock(request,profile_name):
    try:
        user = User.objects.filter(Profile_name = profile_name).first()
    except Gig.DoesNotExist:
        raise Http404("User not found")

    user.is_active = True
    user.save()
    return redirect("control_panel:freelancers" )
        

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def freelancer_view_profile(request,profile_name):
    user = User.objects.filter(Profile_name = profile_name).first()
    profile = Freelancer_Profile.objects.get(user_id = user)
    gigs = Gig.objects.filter(freelancer_id = user)
    gig_count = gigs.count()
    user_subscriptions = UserSubscription.objects.filter(user = user)
    return render(request,"management/freelancer-detail.html",{"user":user,"profile":profile,"count":gig_count,"user_subscriptions":user_subscriptions})



@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def freelancer_gig_list(request,profile_name):
    user = User.objects.filter(Profile_name = profile_name).first()
    gigs = Gig.objects.filter(freelancer_id = user)
    return render(request,"management/freelancer-gigs-list.html",{"user":user,"gigs":gigs})





































@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def total_gigs(request):
    gigs = Gig.objects.all()
    if request.method == "GET":
        search_keyword = request.GET.get("search")
        category = request.GET.get("category")
        skills = request.GET.get("skills")
        date_status = request.GET.get("sort")
        gig_status = request.GET.get("status")
        minimum_price = request.GET.get("min_price")
        maximum_price = request.GET.get("max_price")
        if search_keyword :
            gigs = gigs.filter(title__icontains = search_keyword )
        if category :
            gigs = gigs.filter(categories__name__icontains = category)
        if skills :
            gigs = gigs.filter(skills__icontains = skills)
        if gig_status :
            if gig_status == "active" :
                gigs = gigs.filter(is_blocked = False)
            if gig_status == "blocked" :
                gigs = gigs.filter(is_blocked = True)
        if date_status:
            if date_status == "newest":
                gigs = gigs.order_by("-created_at")
            if date_status == "oldest":
                gigs = gigs.order_by("created_at")
        if minimum_price and maximum_price :
            gigs = gigs.filter(price_min__gte = minimum_price,price_max__lte = maximum_price)        
    return render(request,"management/all-gigs.html",{"gigs":gigs})
































@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def gig_block(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = True
    gig.save()
    return redirect("control_panel:freelancer_gig_list",gig.freelancer_id.Profile_name )


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def gig_block2(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = True
    gig.save()
    return redirect("control_panel:view_gig",gig.slug )


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def gig_block3(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = True
    gig.save()
    return redirect("control_panel:all_gig_list")


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def gig_unblock(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = False
    gig.save()
    return redirect("control_panel:freelancer_gig_list",gig.freelancer_id.Profile_name )


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def gig_unblock2(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = False
    gig.save()
    return redirect("control_panel:view_gig",gig.slug )


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def gig_unblock3(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")

    gig.is_blocked = False
    gig.save()
    return redirect("control_panel:all_gig_list")



@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def view_gig(request,slug):
    try:
        gig = Gig.objects.get(slug=slug)
    except Gig.DoesNotExist:
        raise Http404("Gig not found")
    gig_images = GigImages.objects.filter(gig_id=gig)
    skills = gig.skills
    skills = skills.split(",")
    return render(request,"management/gig-detail.html",{"gig":gig,"gig_images":gig_images,"skills":skills})



@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
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



@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def category_block(request,slug):
    category = Categories.objects.get(slug = slug)
    category.is_blocked = True
    category.save()
    return redirect("control_panel:categories")


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def category_unblock(request,slug):
    category = Categories.objects.get(slug = slug)
    category.is_blocked = False
    category.save()
    return redirect("control_panel:categories")


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def category_delete(request,slug):
    category = Categories.objects.get(slug = slug)
    category.delete()
    return redirect("control_panel:categories")
















@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def clients(request):
    clients = User.objects.filter(role = "client")
    if request.method == "GET":
        search_keyword = request.GET.get("search")
        verification_status = request.GET.get("verified")
        account_status = request.GET.get("blocked")
        date_status = request.GET.get("sort")
        if search_keyword :
            if is_email(search_keyword):
                clients = clients.filter(email__icontains = search_keyword)
            else :
                clients = clients.filter(Profile_name__icontains = search_keyword)
        if verification_status :
            if verification_status == "verified":
                clients = clients.filter(is_verified = True)
            elif verification_status == "not_verified":
                clients = clients.filter(is_verified = False)
            
        if account_status :
            if account_status == "blocked":
                clients = clients.filter(is_active=False)
            elif account_status == "unblocked":
                clients = clients.filter(is_active=True)
        if date_status :
            if date_status == "newest" :
                clients = clients.order_by("-date_joined")
            elif date_status == "oldest" :
                clients = clients.order_by("date_joined")
        
    return render(request,"management/clients/clients.html",{"clients":clients})




















@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def client_block(request,profile_name):
    try:
        client = User.objects.filter(Profile_name = profile_name).first()
    except User.DoesNotExist:
        raise Http404("User not found")

    client.is_active = False
    client.save()
    return redirect("control_panel:clients")


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def client_unblock(request,profile_name):
    try:
        client = User.objects.filter(Profile_name = profile_name).first()
    except User.DoesNotExist:
        raise Http404("User not found")

    client.is_active = True
    client.save()
    return redirect("control_panel:clients")





@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
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



@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def client_wallet_transactions(request,profile_name):
    client = User.objects.get(Profile_name = profile_name)
    wallet = Wallet.objects.get(user = client)
    txns = WalletTransactions.objects.filter(wallet = wallet)
    return render(request,"management/clients/client-wallet-transactions.html",{"client":client,"txns":txns})


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def txn_update(request,id):
    if request.method == "POST":
        status = request.POST.get("status")
        txn = WalletTransactions.objects.get(id = id)
        txn.status = status
        txn.save()
        return redirect("control_panel:client_wallet_transactions",txn.wallet.user.Profile_name)

    return render(request,"management/clients/client-wallet-transactions.html",{"client":None,"txns":WalletTransactions.objects.none()}) 
    

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def freeze_wallet(request,id):
    wallet = Wallet.objects.get(id = id)
    wallet.is_blocked = True
    wallet.save()
    return redirect("control_panel:client_profile",wallet.user.Profile_name )
       

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def unfreeze_wallet(request,id):
    wallet = Wallet.objects.get(id = id)
    wallet.is_blocked = False
    wallet.save()
    return redirect("control_panel:client_profile",wallet.user.Profile_name )


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def client_cards_list(request,profile_name):
    
    user = User.objects.filter(Profile_name = profile_name).first()
    cards = Card.objects.filter(client_id = user)
    return render(request,"management/clients/client-cards-list.html",{"user":user,"cards":cards})
    
    

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def card_block(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = True
    card.save()
    return redirect("control_panel:client_cards_list",card.client_id.Profile_name)


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def card_block2(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = True
    card.save()
    return redirect("control_panel:view_card",card.slug)


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def card_block3(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = True
    card.save()
    return redirect("control_panel:all_cards_list")


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def card_unblock(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = False
    card.save()
    return redirect("control_panel:client_cards_list",card.client_id.Profile_name )


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def card_unblock2(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = False
    card.save()
    return redirect("control_panel:view_card",card.slug )


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def card_unblock3(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")

    card.is_blocked = False
    card.save()
    return redirect("control_panel:all_cards_list")






@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def view_card(request,slug):
    try:
        card = Card.objects.get(slug=slug)
    except Card.DoesNotExist:
        raise Http404("Gig not found")
    card_images = Card_images.objects.filter(card_id=card)
    skills = card.skills_required
    skills = skills.split(",")
    return render(request,"management/clients/card-detail.html",{"card":card,"card_images":card_images,"skills":skills})
















@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def total_cards(request):
    cards = Card.objects.all()
    if request.method == "GET":
        search_keyword = request.GET.get("search")
        category = request.GET.get("category")
        skills = request.GET.get("skills")
        date_status = request.GET.get("sort")
        card_status = request.GET.get("status")
        minimum_price = request.GET.get("min_price")
        maximum_price = request.GET.get("max_price")
        time_line = request.GET.get("timeline")
        if search_keyword :
            cards = cards.filter(title__icontains = search_keyword )
        if category :
            cards = cards.filter(category__name__icontains = category)
        if skills :
            cards = cards.filter(skills_required__icontains = skills)
        if time_line:
            cards = cards.filter(time_line__icontains = time_line)
        if card_status :
            if card_status == "active" :
                cards = cards.filter(is_blocked = False)
            if card_status == "blocked" :
                cards = cards.filter(is_blocked = True)
        if date_status:
            if date_status == "newest":
                cards = cards.order_by("-created_at")
            if date_status == "oldest":
                cards = cards.order_by("created_at")
        if minimum_price and maximum_price :
            cards = cards.filter(min_budget__gte = minimum_price,max_budget__lte = maximum_price)
    return render(request,"management/clients/all-cards.html",{"cards":cards})





















@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def logout(request):
    request.session.flush()
    return redirect("accounts:landing_page")


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def subscriptions(request):
    subscriptions = SubscriptionPack.objects.all()
    plantypes = Plantype.objects.all()
    return render(request,"management/subscription_list.html",{"subscriptions":subscriptions,"plantypes":plantypes})


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
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



@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
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



@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def disable_subscription(request,slug):
    if request.method == "POST":
        next_url = request.POST.get("next")
        subscriptionpack = SubscriptionPack.objects.filter(slug = slug).first()
        subscriptionpack.is_active = False
        subscriptionpack.save()
        return redirect(next_url)
    

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def enable_subscription(request,slug):
    if request.method == "POST":
        next_url = request.POST.get("next")
        subscriptionpack = SubscriptionPack.objects.filter(slug = slug).first()
        subscriptionpack.is_active = True
        subscriptionpack.save()
        return redirect(next_url)
    
    


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def delete_subscription(request,slug):
    if request.method == "POST":
        next_url = request.POST.get("next")
        subscriptionpack = SubscriptionPack.objects.filter(slug = slug).first()
        subscriptionpack.delete()
        return redirect(next_url)
    
    

@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def edit_plantype(request):
    plantype_id = request.POST.get("id")
    # print(request.POST)
    # print(plantype_id)
    plantype = Plantype.objects.get(id = plantype_id)

    form = EditPlanTypeForm(request.POST, instance=plantype)

    if form.is_valid():
        updated = form.save()
        return JsonResponse({
            "success": True,
            "id": updated.id,
            "name": updated.name,
        })

    return JsonResponse({
        "success": False,
        "errors": form.errors,
    }, status=400)
    


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def delete_plantype(request,name):
    plantype = get_object_or_404(Plantype,name = name)
    next_url = request.POST.get("next")
    plantype.delete()
    return redirect(next_url)
    


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def enable_plantype(request,name):
    plantype = get_object_or_404(Plantype,name = name)
    next_url = request.POST.get("next")
    plantype.is_active = True
    plantype.save()
    return redirect(next_url)


@login_required(login_url=reverse_lazy('control_panel:signin')) 
@never_cache 
def disable_plantype(request,name):
    plantype = get_object_or_404(Plantype,name = name)
    next_url = request.POST.get("next")
    plantype.is_active = False
    plantype.save()
    return redirect(next_url)
    
    

def service_pricing(request):
    pricing,_ = Pricing.objects.get_or_create(id = 1)
    if request.method == "POST" :
        card_creation_price = request.POST.get("card_creation_price")
        connection_price = request.POST.get("connection_price")
        form = PricingForm(request.POST)
        if form.is_valid() :
            pricing = Pricing.objects.update_or_create(id = 1,
                                                    defaults = {
                                                        "card_creation_price" : card_creation_price,
                                                        "connection_price" : connection_price
                                                    })
    else :
        form = PricingForm(instance = pricing)
    return render(request,"management/service_pricing.html",{"form":form,"pricing":pricing})




def freelancer_connections(request,id):
    user = User.objects.get(id = id)
    connections = Connections.objects.filter(user = user)
    return render(request,"management/freelancer-connections.html",{"connections":connections})


def client_connections(request,id):
    user = User.objects.get(id = id)
    connections = Connections.objects.filter(client_user = user)
    return render(request,"management/clients/client-connections.html",{"connections":connections})