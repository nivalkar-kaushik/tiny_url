from django.contrib import admin
from .models import User, EmailOTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_verified", "date_joined")
    search_fields = ("username", "email")

@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "is_used", "created_at")
