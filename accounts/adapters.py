# your_app/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()
from django.shortcuts import redirect


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Called just after successful authentication from provider,
        but before the actual login happens.
        """
        print("Ivide ethi")

        email = sociallogin.user.email
        print(email)

        # If provider didn't send email, skip this logic.
        if not email:
            return

        try:
            existing_user = User.objects.get(email=email)
        except User.DoesNotExist:
            # No user with this email yet → allow normal social signup
            return

        # If there *is* already a user with this email, but no social account
        # for this provider, then show the custom error page.
        provider = sociallogin.account.provider  # like "google"

        has_social_for_provider = existing_user.socialaccount_set.filter(
            provider=provider
        ).exists()

        if not has_social_for_provider:
            # Stop the pipeline and return a custom response
            response = redirect('accounts:social_email_conflict')
            raise ImmediateHttpResponse(response)
