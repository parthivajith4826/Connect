from django.urls import path
from . import views


app_name = 'control_panel'
urlpatterns = [
    path('',views.signin,name = 'signin'),
    path('dashboard/',views.home,name = 'home'),
    path('pending-transactions/',views.pending_transactions,name = 'pending-transactions'),
    path('freelancers/',views.freelancers,name = 'freelancers'),
    path('clients/',views.clients,name = 'clients'),
    path('freelancer-profile/<str:profile_name>',views.freelancer_view_profile,name = 'freelancer_profile'),
    path('client-profile/<str:profile_name>',views.client_view_profile,name = 'client_profile'),
    path('freelancer-gigs-list/<str:profile_name>',views.freelancer_gig_list,name = 'freelancer_gig_list'),
    path('all-gigs-list/',views.total_gigs,name = 'all_gig_list'),
    path('gig-block/<slug:slug>',views.gig_block,name = 'gig_block'),
    path('gig-block2/<slug:slug>',views.gig_block2,name = 'gig_block2'),
    path('gig-block3/<slug:slug>',views.gig_block3,name = 'gig_block3'),
    path('gig-unblock/<slug:slug>',views.gig_unblock,name = 'gig_unblock'),
    path('gig-unblock2/<slug:slug>',views.gig_unblock2,name = 'gig_unblock2'),
    path('gig-unblock3/<slug:slug>',views.gig_unblock3,name = 'gig_unblock3'),
    path('freelancer-block/<str:profile_name>',views.freelancer_block,name = 'freelancer_block'),
    path('freelancer-unblock/<str:profile_name>',views.freelancer_unblock,name = 'freelancer_unblock'),
    path('client-block/<str:profile_name>',views.client_block,name = 'client_block'),
    path('client-unblock/<str:profile_name>',views.client_unblock,name = 'client_unblock'),
    path('view-gig/<slug:slug>',views.view_gig,name = 'view_gig'),
    path('categories/',views.categories,name = 'categories'),
    path('category-block/<slug:slug>',views.category_block,name = 'category_block'),
    path('category-unblock/<slug:slug>',views.category_unblock,name = 'category_unblock'),
    path('category-delete/<slug:slug>',views.category_delete,name = 'category_delete'),
    
    
    path("client-wallet-transactions/<str:profile_name>",views.client_wallet_transactions,name = "client_wallet_transactions"),
    path("txn-update/<int:id>",views.txn_update,name = "txn_update"),
    path("freeze-wallet/<int:id>",views.freeze_wallet,name = "freeze_wallet"),
    path("unfreeze-wallet/<int:id>",views.unfreeze_wallet,name = "unfreeze_wallet"),
    
    
    
    path('client-cards-list/<str:profile_name>',views.client_cards_list,name = 'client_cards_list'),
    path('card-block/<slug:slug>',views.card_block,name = 'card_block'),
    path('card-block2/<slug:slug>',views.card_block2,name = 'card_block2'),
    path('card-block3/<slug:slug>',views.card_block3,name = 'card_block3'),
    path('card-unblock/<slug:slug>',views.card_unblock,name = 'card_unblock'),
    path('card-unblock2/<slug:slug>',views.card_unblock2,name = 'card_unblock2'),
    path('card-unblock3/<slug:slug>',views.card_unblock3,name = 'card_unblock3'),
    path('view-card/<slug:slug>',views.view_card,name = 'view_card'),
    
    path('all-cards-list/',views.total_cards,name = 'all_cards_list'),
    
    path("logout/",views.logout,name = "logout"),
    path("subscriptions/",views.subscriptions,name = "subscriptions"),
    path("create-subscriptions/",views.create_subscriptions,name = "create_subscriptions"),
    path("edit-subscription/<slug:slug>",views.edit_subscription,name = "edit_subscription"),
    path("disable-subscription/<slug:slug>",views.disable_subscription,name = "disable_subscription"),
    path("enable-subscription/<slug:slug>",views.enable_subscription,name = "enable_subscription"),
    path("delete-subscription/<slug:slug>",views.delete_subscription,name = "delete_subscription"),
    
    path("edit-plantype/",views.edit_plantype,name = "edit_plantype"),    
    
   ] 
