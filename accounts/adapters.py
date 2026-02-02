from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        email = sociallogin.user.email

        if not email:
            return

        try:
            existing_user = User.objects.get(email=email)
        except User.DoesNotExist:

            return

        provider = sociallogin.account.provider  # like "google"

        has_social_for_provider = existing_user.socialaccount_set.filter(
            provider=provider
        ).exists()

        if not has_social_for_provider:
            response = redirect("accounts:social_email_conflict")
            raise ImmediateHttpResponse(response)
