from .models import User, EmailOTP
from django import forms
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Username"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Email"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Password"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Confirm Password"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

 
# --------------------- registration form using model form   
# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)
    
#     class Meta:
#         model = User
#         fields = ("username", "email")
        
#     def clean(self):
#         cleaned_data = super().clean()
#         if cleaned_data.get("password1") != cleaned_data.get("password2"):
#             raise forms.ValidationError("Passwords do not matched !!")
#         return cleaned_data
        
#     def save(self, commit = False):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data.get("password1"))
#         if commit:
#             user.save()
#         return user

    
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Username",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Password",
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise forms.ValidationError("Your email is not verified. Please check your inbox for the OTP email sent during signup.")

        self.user = user
        return cleaned_data


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 border rounded-md text-center tracking-widest text-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "123456"
        })
    )
    
    def __init__(self, user,  *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_otp(self):
        user_entered_otp = self.cleaned_data["otp"]
        
        #check the Email otp model for user otp combo
        otp = EmailOTP.objects.filter(
            user = self.user,
            otp = user_entered_otp,
        ).order_by("-created_at").first()
        
        if not otp:
            raise forms.ValidationError("Invalid OTP")
        
        if otp.is_expired():
            raise forms.ValidationError("OTP Expired")
        self.otp = otp

        return user_entered_otp