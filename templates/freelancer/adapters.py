from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages

class NoMessageAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        # Disable all default allauth messages
        pass
