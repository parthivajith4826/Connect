from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("register/", views.register, name="register"),
    path("signin/", views.signin, name="signin"),
    path("request-otp/", views.request_otp, name="request_otp"),
    path("otp/", views.otp, name="otp"),
    path("resent-otp/", views.resent_otp, name="resent_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("verify_email/<uuid:token>/", views.verify_email, name="verify_email"),
    path("role/", views.role, name="role"),
    path(
        "login-method-error/", views.social_email_conflict, name="social_email_conflict"
    ),
    path("resend_email/", views.resent_email, name="resent_email"),
    # footer
    path("how-to-hire/", views.how_to_hire, name="how_to_hire"),
    path("talent-marketplace/", views.talent_marketplace, name="talent_marketplace"),
    path("enterprise/", views.enterprise, name="enterprise"),
    path("howto-find-work/", views.how_to_find_work, name="how_to_find_work"),
    path("direct-contracts/", views.direct_contracts, name="direct_contracts"),
    path("community/", views.community, name="community"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
]
