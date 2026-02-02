from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from client.views import stripe_webhook
from freelancer import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("freelancer/", include("freelancer.urls")),
    path("client/", include("client.urls")),
    # allauth
    path("accounts/", include("allauth.urls")),
    path("control-panel/", include("management.urls")),
    path("stripe/webhook/wallet/", stripe_webhook, name="stripe_webhook"),
    path(
        "stripe/webhook/subscription/",
        views.stripe_webhook_subscription,
        name="stripe_webhook_subscription",
    ),
    path("quill/upload-image/", views.quill_image_upload, name="quill_image_upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
