from django import forms
from accounts.models import User
from . models import Freelancer_Profile

from django.core.exceptions import ValidationError
import re
from django.core.files.uploadedfile import UploadedFile
import ast # ast.literal_eval is a safe Python parser.It takes a string that looks like a Python value and converts it into a real Python object


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("profile_photo","Profile_name")
        # widgets = {
        #     'Profile_name': forms.TextInput(attrs={'class':'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'}),
        #     'profile_photo': forms.FileInput(attrs={'class':"hidden" , 'id': 'imageInput',"accept": "image/*"}),
        # }
        
    def clean_Profile_name(self):
        Profile_name = self.cleaned_data.get('Profile_name')
        print(Profile_name)
        
        if not Profile_name:
            
            raise forms.ValidationError("Username required")
        
        
        
        if ' ' in Profile_name:
            
            raise forms.ValidationError("Spaces are not allowed")
            
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9_]{3,}$"
        if not re.match(pattern,Profile_name):
            
            raise forms.ValidationError("Username must contain at least 3 characters, including uppercase, lowercase, and numbers .")
        
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








class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Freelancer_Profile
        fields = ("T_user_name","phone_number")
        
    def clean_T_user_name(self):
        
        username = self.cleaned_data.get('T_user_name')
        
        
        if not username:
            raise forms.ValidationError("Username cant be empty!")
        print(username)
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]{3,30}[a-zA-Z0-9]$'
        if not re.match(pattern,username):
            raise forms.ValidationError('Invalid Telegram Username')
        
        return username
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        print(phone_number)
        if not phone_number :
            raise forms.ValidationError("Mobile number field cant be empty!")
        
        pattern = r'^[1-9]\d{9}$'
        if not re.match(pattern,phone_number):
            raise forms.ValidationError("Invalid Mobile Number")        
    
        return phone_number
        
    