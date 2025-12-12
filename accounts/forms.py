from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
import re

class SignupForm(UserCreationForm):
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-3 py-3 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors',
            'placeholder': '••••••••',
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-3 py-3 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors',
            'placeholder': '••••••••',
        })
    )
    
    
    
    class Meta:
        model = User
        fields = ['email','password1','password2']
        
        widgets = {
            'email': forms.EmailInput(attrs={'class':'appearance-none block w-full px-3 py-3 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors',
                'placeholder': 'Enter your email',
            }),
        }
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        
        if ' ' in password:
            raise forms.ValidationError("Password cannot contain spaces.")
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z1-9@$!%*?&#]{8,}$"
        if not re.match(pattern,password):
            raise forms.ValidationError("Password must contain at least 8 characters, including uppercase, lowercase, and numbers.")
        return password
        

class Reset_passwordForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'appearance-none block w-full px-3 py-3 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors',
            'placeholder': '••••••••',
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'appearance-none block w-full px-3 py-3 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-colors',
            'placeholder': '••••••••',
        })
    )


    class Meta:
        model = User
        fields = ['password1','password2']
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        
        if ' ' in password:
            raise forms.ValidationError("Spaces are not allowed in password")
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z1-9@$!%*?&#]{8,}$"
        if not re.match(pattern,password):
            raise forms.ValidationError("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one number.")
        return password