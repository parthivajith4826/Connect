import re
from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from accounts.models import User

from .models import Freelancer_Profile, Gig


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("profile_photo", "Profile_name")

    def clean_Profile_name(self):
        Profile_name = self.cleaned_data.get("Profile_name")

        if not Profile_name:

            raise forms.ValidationError("Username required")

        if " " in Profile_name:

            raise forms.ValidationError("Spaces are not allowed")

        pattern = r"^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9_]{3,}$"
        if not re.match(pattern, Profile_name):

            raise forms.ValidationError(
                "Username must contain at least 3 characters, including uppercase, lowercase, and numbers ."
            )

        return Profile_name

    def clean_profile_photo(self):

        profile_photo = self.cleaned_data.get("profile_photo")

        if not profile_photo and not self.instance.profile_photo:
            raise forms.ValidationError("Image not selected")

        if isinstance(profile_photo, UploadedFile):
            if profile_photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image too large (max 2MB)")

            if profile_photo.content_type not in ("image/jpeg", "image/png"):
                raise forms.ValidationError("Only JPG/PNG allowed")

        return profile_photo


class ContactForm(forms.ModelForm):

    class Meta:
        model = Freelancer_Profile
        fields = ("T_user_name", "phone_number")

    def clean_T_user_name(self):

        username = self.cleaned_data.get("T_user_name")

        if not username:
            raise forms.ValidationError("Username cant be empty!")
        pattern = r"^[a-zA-Z][a-zA-Z0-9_]{3,30}[a-zA-Z0-9]$"
        if not re.match(pattern, username):
            raise forms.ValidationError("Invalid Telegram Username")

        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            raise forms.ValidationError("Mobile number field cant be empty!")

        pattern = r"^[1-9]\d{9}$"
        if not re.match(pattern, phone_number):
            raise forms.ValidationError("Invalid Mobile Number")

        return phone_number


class CreategigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = (
            "title",
            "portfolio",
            "price_max",
            "price_min",
            "skills",
            "description",
            "categories",
        )

    def clean_title(self):

        title = self.cleaned_data.get("title")

        if not title:
            raise ValidationError("Job title is required.")

        if len(title) < 5:
            raise ValidationError("Job title must be at least 5 characters.")

        return title

    def clean_skills(self):
        skills = self.cleaned_data.get("skills")
        if not skills:
            raise ValidationError("Skills are required.")

        skills_list = [s.strip() for s in skills.split(",") if s.strip()]

        if len(skills_list) < 2:
            raise ValidationError("Enter at least 2 skills separated by commas.")
        return ",".join(skills_list)

    def clean_description(self):
        description = self.cleaned_data.get("description")

        if not description or len(description.strip()) < 20:
            raise ValidationError("Description must be at least 20 characters.")

        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        phone_pattern = r"(\+?\d{1,3}[\s-]?)?\d{10}"

        if re.search(email_pattern, description):
            raise ValidationError("Email addresses are not allowed in the description.")

        if re.search(phone_pattern, description):
            raise ValidationError("Phone numbers are not allowed in the description.")

        return description

    def clean(self):
        cleaned_data = super().clean()

        price_max = cleaned_data.get("price_max")
        price_min = cleaned_data.get("price_min")

        if price_min is not None and price_max is not None:

            if price_min <= 0:
                self.add_error("price_min", "Min budget must be greater than zero.")

            if price_max <= 0:
                self.add_error("price_max", "Max budget must be greater than zero.")

            if price_min == price_max:
                self.add_error(None, "Min and max budget cannot be the same.")

            if price_min > price_max:
                self.add_error(None, "Min budget must be less than max budget.")

        return cleaned_data

    def clean_portfolio(self):
        link = self.cleaned_data.get("portfolio")

        if not link:
            return link

        parsed_url = urlparse(link)

        if parsed_url.scheme not in ["http", "https"]:
            raise ValidationError("Portfolio link must start with http:// or https://")

        if " " in link:
            raise ValidationError("Portfolio link must not contain spaces.")
        return link
