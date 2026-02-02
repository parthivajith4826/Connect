from django.urls import path

from . import views

app_name = "freelancer"
urlpatterns = [
    path("", views.home, name="home"),
    path("signout/", views.signout, name="signout"),
    path("profile/", views.profile, name="profile"),
    # path('gigs/',views.gigs,name = 'gigs'),
    path("add-gig/", views.add_gig, name="add_gig"),
    path("view-gig/<str:slug>", views.view_gig, name="view_gig"),
    path("edit-gig/<str:slug>", views.edit_gig, name="edit_gig"),
    path("close-gig/<str:slug>", views.close_gig, name="close_gig"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("subscribe-start/<slug:slug>", views.subscribe_start, name="subscribe_start"),
    path("subscription/result/", views.subscription_result, name="subscription_result"),
    path("find-work", views.find_work, name="find_work"),
    path("work-details/<slug:slug>", views.card_details, name="work_details"),
    path("show-gigs/<slug:card_slug>", views.show_gigs, name="show_gigs"),
    path(
        "create-connection/<slug:card_slug>",
        views.create_connection,
        name="create_connection",
    ),
    path(
        "show-gig-details/<slug:slug>", views.show_gig_details, name="show_gig_details"
    ),
    path(
        "subscription-details/", views.subscription_details, name="subscription_details"
    ),
    path("my-connections/", views.my_connections, name="my_connections"),
    path("gig-preview/<slug:slug>", views.gig_preview, name="gig_preview"),
]
