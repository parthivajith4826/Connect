
from django import forms
from django.core.exceptions import ValidationError
from client.models import Categories
from .models import SubscriptionPack,Plantype
import re


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name or len(name.strip()) < 3:
            raise forms.ValidationError(
                "Category name must be at least 3 characters long."
            )

        if not re.match(r"^[A-Za-z ]+$", name):
            raise forms.ValidationError(
                "Category name can contain only letters and spaces."
            )

        if Categories.objects.filter(name__iexact=name.strip()).exists():
            raise forms.ValidationError("This category already exists.")

        return name.strip()
    
    
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPack
        fields = ["title","plantype","max_gigs","max_images_per_gig","connection_limit","duration_days","price","is_free"]
        
        
    def clean_title(self):
        title = self.cleaned_data.get("title")

        if not title:
            raise ValidationError("Title is required.")

        title = title.strip()

        # # No spaces inside
        # if " " in title:
        #     raise ValidationError("Spaces are not allowed in the title.")

        # Length check
        if len(title) < 3:
            raise ValidationError("Title must be at least 3 characters long.")

        # block special characters
        if not re.match(r'^[A-Za-z ]+$', title):
            raise ValidationError("Only letters are allowed.")
        
        
        if SubscriptionPack.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError("This title already exists.")

        return title

    def clean_max_gigs(self):
        value = self.cleaned_data.get("max_gigs")

        if value is None or value < 1:
            raise ValidationError("Max gigs must be at least 1.")

        return value

    def clean_max_images_per_gig(self):
        value = self.cleaned_data.get("max_images_per_gig")

        if value is None or value < 1:
            raise ValidationError("Max images per gig must be at least 1.")

        return value

    def clean_connection_limit(self):
        value = self.cleaned_data.get("connection_limit")

        if value is None or value < 1:
            raise ValidationError("Connection limit must be at least 1.")

        return value

    def clean_duration_days(self):
        value = self.cleaned_data.get("duration_days")

        if value is None or value < 1:
            raise ValidationError("Duration must be at least 1 day.")

        return value

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is None:
            raise ValidationError("Price is required.")

        if price < 0:
            raise ValidationError("Price cannot be negative.")

        return price

    

    def clean(self):
        cleaned_data = super().clean()

        price = cleaned_data.get("price")
        is_free = cleaned_data.get("is_free")

        # Free plan logic
        if is_free:
            if price != 0:
                raise ValidationError(
                    "Free plans must have a price of 0."
                )
        else:
            if price == 0:
                raise ValidationError(
                    "Paid plans must have a price greater than 0."
                )

        return cleaned_data



class EditSubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPack
        fields = ["title","plantype","max_gigs","max_images_per_gig","connection_limit","duration_days","price","is_free"]
        
        
    def clean_title(self):
        title = self.cleaned_data.get("title")
        print(title)

        if not title:
            raise ValidationError("Title is required.")

        title = title.strip()

        # # No spaces inside
        # if " " in title:
        #     raise ValidationError("Spaces are not allowed in the title.")

        # Length check
        if len(title) < 3:
            raise ValidationError("Title must be at least 3 characters long.")

        # block special characters
        if not re.match(r'^[A-Za-z ]+$', title):
            raise ValidationError("Only letters are allowed.")

        return title

    def clean_max_gigs(self):
        value = self.cleaned_data.get("max_gigs")

        if value is None or value < 1:
            raise ValidationError("Max gigs must be at least 1.")

        return value

    def clean_max_images_per_gig(self):
        value = self.cleaned_data.get("max_images_per_gig")

        if value is None or value < 1:
            raise ValidationError("Max images per gig must be at least 1.")

        return value

    def clean_connection_limit(self):
        value = self.cleaned_data.get("connection_limit")

        if value is None or value < 1:
            raise ValidationError("Connection limit must be at least 1.")

        return value

    def clean_duration_days(self):
        value = self.cleaned_data.get("duration_days")

        if value is None or value < 1:
            raise ValidationError("Duration must be at least 1 day.")

        return value

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is None:
            raise ValidationError("Price is required.")

        if price < 0:
            raise ValidationError("Price cannot be negative.")

        return price

    

    def clean(self):
        cleaned_data = super().clean()

        price = cleaned_data.get("price")
        is_free = cleaned_data.get("is_free")

        # Free plan logic
        if is_free:
            if price != 0:
                raise ValidationError(
                    "Free plans must have a price of 0."
                )
        else:
            if price == 0:
                raise ValidationError(
                    "Paid plans must have a price greater than 0."
                )

        return cleaned_data



class PlanTypeForm(forms.ModelForm):
    class Meta:
        model = Plantype
        fields = ["name", "description"]


    def clean_name(self):
        name = self.cleaned_data.get("name")
        print(name)
        if not name:
            raise ValidationError("Plan type name is required.")

        name = name.strip()

        if len(name) < 2:
            raise ValidationError("Minimum 2 characters should be there.")

        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError("Only letters are allowed.")
        
        
        if Plantype.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This title already exists.")

        return name

    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        print(description)

        # Description is optional
        if not description:
            return description

        description = description.strip()

        # Prevent only spaces
        if len(description) == 0:
            raise ValidationError("Description cannot be empty.")

        # Minimum length
        if len(description) < 10:
            raise ValidationError(
                "Description must be at least 10 characters long."
            )

        # Maximum length
        if len(description) > 300:
            raise ValidationError(
                "Description cannot exceed 300 characters."
            )

        # Block email addresses
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        if re.search(email_pattern, description):
            raise ValidationError("Email addresses are not allowed.")

        # Block phone numbers
        phone_pattern = r"(\+?\d{1,3}[\s-]?)?\d{10}"
        if re.search(phone_pattern, description):
            raise ValidationError("Phone numbers are not allowed.")

        return description