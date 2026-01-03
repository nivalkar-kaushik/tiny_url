from django.db import models
from accounts.models import User
import string
import random
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class ShortURL(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="short_urls"
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)

    original_url = models.URLField()
    code = models.CharField(max_length=10, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.code} → {self.original_url}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_short_code()
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("links:redirect_short_url", args=[self.code])

    
    @staticmethod
    def generate_short_code(length=6):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))
        


class ClickAnalytics(models.Model):
    short_url = models.ForeignKey(
        "ShortURL",
        on_delete=models.CASCADE,
        related_name="clicks"
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    device_type = models.CharField(max_length=20)
    browser = models.CharField(max_length=50)
    os = models.CharField(max_length=50)

    country = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.short_url.code} - {self.ip_address}"


