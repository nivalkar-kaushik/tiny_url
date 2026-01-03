from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm, LoginForm, OTPForm
from .models import User, EmailOTP
import random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def send_email_otp(user):
    code = str(random.randint(100000, 999999))
    otp = EmailOTP.objects.create(
        user = user,
        otp = code
    )
    # TODO: send otp to user email
    print("--------------------------otp", otp.otp)
    
def signup_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            request.session["verified_user_id"] = user.id
            send_email_otp(user)
            return redirect("accounts:verify_otp")
    else:
        form = RegistrationForm()
    return render(request , "accounts/registration.html",{"form":form})

def verify_otp_view(request):
    user_id = request.session.get("verified_user_id")
    if not user_id:
        return HttpResponse("no user id found in session")
    user = User.objects.get(id = user_id)
    if request.method == "POST":
        
        form = OTPForm(user, request.POST)
        if form.is_valid():
            otp = form.otp
            otp.is_used = True
            otp.save()
            
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect("links:home")
    else:
        form = OTPForm(user)
    return render(request, "accounts/verify_otp.html", {"form":form})
    

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)
            return redirect("links:home")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")