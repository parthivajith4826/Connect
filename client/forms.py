from django import forms
from accounts.models import User
from .models import Location,Card
from django.core.exceptions import ValidationError
import re
from django.core.files.uploadedfile import UploadedFile
import ast # ast.literal_eval is a safe Python parser.It takes a string that looks like a Python value and converts it into a real Python object


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("profile_photo","Profile_name")
        widgets = {
            'Profile_name': forms.TextInput(attrs={'class':'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'}),
            'profile_photo': forms.FileInput(attrs={'class':"hidden" , 'id': 'imageInput',"accept": "image/*"}),
        }
        
    def clean_Profile_name(self):
        Profile_name = self.cleaned_data.get('Profile_name')
        # print(Profile_name)
        
        if not Profile_name:
            
            raise forms.ValidationError("Username required")
        
        if ' ' in Profile_name:
            
            raise forms.ValidationError("Spaces are not allowed")
            
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9_]{3,}$"
        if not re.match(pattern,Profile_name):
            
            raise forms.ValidationError("Username must contain at least 3 characters, including uppercase, lowercase, and numbers only.")
        
        return Profile_name
    
    def clean_profile_photo(self):
        
        profile_photo = self.cleaned_data.get('profile_photo')

        if not profile_photo and not self.instance.profile_photo:
            raise forms.ValidationError("Image not selected")

        print(type(profile_photo))
        
        if isinstance(profile_photo, UploadedFile):
            if profile_photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image too large (max 2MB)")

            if profile_photo.content_type not in ("image/jpeg", "image/png"):
                raise forms.ValidationError("Only JPG/PNG allowed")
        
        return profile_photo
    
    
    
    
    
    
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("location_name","latitude","longitude")
        widgets = {'location_name':forms.TextInput(attrs={'id':'location','placeholder':'Use current location','readonly':'readonly','class':'w-full px-4 py-2 border rounded-lg'}),
                'latitude':forms.HiddenInput(attrs={'id':'lat'}),
                'longitude':forms.HiddenInput(attrs={'id':'lng'}),
                }
    
    
    def clean_location_name(self):
        location_name = self.cleaned_data.get('location_name')
        
        if not location_name:   
            raise forms.ValidationError("Please select your location using the button")
        
        return location_name
    
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        # print(latitude)
        
        if not latitude: 
            raise forms.ValidationError("Latitude not found. Please fetch location again.")
            
        if not (-90 <= latitude <= 90):
            raise forms.ValidationError("Invalid latitude value.")

        return latitude
    
    
    def clean_longitude(self):
        longitude = self.cleaned_data.get("longitude")
        # print(longitude)
        if longitude is None:
            raise forms.ValidationError("Longitude not found. Please fetch location again.")

        if not (-180 <= longitude <= 180):
            raise forms.ValidationError("Invalid longitude value.")

        return longitude
    
    
    
class CreatecardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ("title","category_id","skills_required","description","min_budget","max_budget","time_line")
        
    def clean_title(self):
        title = self.cleaned_data.get("title")
        # print(title)

        if not title:
            raise ValidationError("Job title is required.")

        if len(title) < 5:
            raise ValidationError("Job title must be at least 5 characters.")
        return title


    def clean_skills_required(self):
        skills = self.cleaned_data.get("skills_required")
        if not skills:
            raise ValidationError("Skills are required.")

        skills_list = [s.strip() for s in skills.split(",") if s.strip()]
        # print(skills_list)

        if len(skills_list) < 2:
            raise ValidationError("Enter at least 2 skills separated by commas.")
        
        return ",".join(skills_list)

    
    def clean_description(self):
        description = self.cleaned_data.get("description")
        # print(description)

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

        min_budget = cleaned_data.get("min_budget")
        max_budget = cleaned_data.get("max_budget")
        # print(min_budget)
        # print(max_budget)

        if min_budget and max_budget:
            
            if min_budget == max_budget:
                raise ValidationError("Provide a valid min and max budget.")
            
            if min_budget <= 0 or max_budget <= 0:
                raise ValidationError("Budget must be greater than zero.")

            if min_budget >= max_budget:
                raise ValidationError("Min budget must be less than max budget.")

        return cleaned_data
    
        
        
            

    
