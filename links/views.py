from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
from ipware import get_client_ip
from user_agents import parse
from .models import ShortURL, ClickAnalytics
from django.db import models
from datetime import datetime
import re
import urllib.request
import urllib.parse
import json

RESERVED_ALIASES = {'create', 'dashboard', 'analytics', 'toggle', 'delete', 'account', 'admin', 'static'}


def verify_recaptcha(token):
    data = urllib.parse.urlencode({
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': token,
    }).encode()
    req = urllib.request.urlopen(
        'https://www.google.com/recaptcha/api/siteverify', data
    )
    return json.loads(req.read().decode()).get('success', False)


def home(request):
    return render(request, "links/home.html", {
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
    })


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def create_short_url(request):
    original_url = request.POST.get("original_url", "").strip()
    custom_alias = request.POST.get("custom_alias", "").strip()

    if not original_url:
        return render(request, "links/error.html", {"error": "Please enter a URL."})

    if not original_url.startswith(("http://", "https://")):
        return render(request, "links/error.html", {"error": "Please enter a valid URL starting with http:// or https://"})

    # CAPTCHA check for anonymous users
    if not request.user.is_authenticated:
        token = request.POST.get('g-recaptcha-response', '')
        if not verify_recaptcha(token):
            return render(request, 'links/error.html', {'error': 'Please complete the CAPTCHA.'})

    # Parse optional expiry date
    expires_at = None
    expires_at_str = request.POST.get("expires_at", "").strip()
    if expires_at_str:
        try:
            naive_dt = datetime.strptime(expires_at_str, "%Y-%m-%d")
            expires_at = timezone.make_aware(naive_dt)
            if expires_at <= timezone.now():
                return render(request, "links/error.html", {"error": "Expiry date must be in the future."})
        except ValueError:
            return render(request, "links/error.html", {"error": "Invalid expiry date."})

    # Parse optional link password
    link_password_raw = request.POST.get("link_password", "").strip()
    link_password = make_password(link_password_raw) if link_password_raw else None

    if custom_alias:
        if not request.user.is_authenticated:
            return render(request, "links/error.html", {"error": "Please log in to use a custom alias."})

        if not re.match(r'^[a-zA-Z0-9-]{3,10}$', custom_alias):
            return render(request, "links/error.html", {"error": "Alias must be 3–10 characters (letters, numbers, hyphens only)."})

        if custom_alias.lower() in RESERVED_ALIASES:
            return render(request, "links/error.html", {"error": f"'{custom_alias}' is a reserved word. Please choose a different alias."})

        if ShortURL.objects.filter(code=custom_alias).exists():
            return render(request, "links/error.html", {"error": f"'{custom_alias}' is already taken. Please choose a different alias."})

        short = ShortURL.objects.create(user=request.user, original_url=original_url, code=custom_alias, expires_at=expires_at, link_password=link_password)
        created = True

    elif expires_at or link_password:
        # Expiry or password set — always create a new record
        user = request.user if request.user.is_authenticated else None
        session_key = None
        if not user:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
        short = ShortURL.objects.create(user=user, session_key=session_key, original_url=original_url, expires_at=expires_at, link_password=link_password)
        created = True

    elif request.user.is_authenticated:
        short, created = ShortURL.objects.get_or_create(
            user=request.user,
            original_url=original_url,
            defaults={}
        )
    else:
        # Anonymous user → use session
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        short, created = ShortURL.objects.get_or_create(
            user=None,
            session_key=session_key,
            original_url=original_url,
            defaults={}
        )

    short_url = request.build_absolute_uri(short.get_absolute_url())

    return render(
        request,
        "links/create.html",
        {
            "short_url": short_url,
            "created": created,
        }
    )

@ratelimit(key='ip', rate='60/m', method=ratelimit.ALL, block=True)
def redirect_short_url(request, code):
    short_url = get_object_or_404(ShortURL, code=code, is_active=True)

    # Check expiry
    if short_url.expires_at and timezone.now() > short_url.expires_at:
        return render(request, "links/expired.html", {"short_url": short_url}, status=410)

    # Password gate
    if short_url.link_password:
        if request.method == "POST":
            entered = request.POST.get("password", "")
            if not check_password(entered, short_url.link_password):
                return render(request, "links/password_gate.html", {
                    "short_url": short_url, "error": "Incorrect password."
                })
            # correct password — fall through to analytics + redirect
        else:
            return render(request, "links/password_gate.html", {"short_url": short_url})

    # Get IP
    ip, _ = get_client_ip(request)

    # User agent parsing
    user_agent_str = request.META.get("HTTP_USER_AGENT", "")
    user_agent = parse(user_agent_str)

    device_type = (
        "mobile" if user_agent.is_mobile else
        "tablet" if user_agent.is_tablet else
        "desktop"
    )

    # Save analytics
    ClickAnalytics.objects.create(
        short_url=short_url,
        ip_address=ip,
        user_agent=user_agent_str,
        device_type=device_type,
        browser=user_agent.browser.family,
        os=user_agent.os.family,
    )

    return redirect(short_url.original_url)

@login_required
def dashboard(request):
    urls = (
        ShortURL.objects
        .filter(user=request.user)
        .annotate(total_clicks=models.Count("clicks"))
        .order_by("-created_at")
    )
    for u in urls:
        u.full_url = request.build_absolute_uri(u.get_absolute_url())

    paginator = Paginator(urls, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "links/dashboard.html", {
        "page_obj": page_obj,
    })

@login_required
def shorturl_analytics(request, pk):
    short_url = get_object_or_404(
        ShortURL,
        id=pk,
        user=request.user
    )

    clicks = short_url.clicks.all()
    clicks_paginator = Paginator(clicks.order_by("-created_at"), 20)
    clicks_page = clicks_paginator.get_page(request.GET.get("page"))

    context = {
        "short_url": short_url,
        "total_clicks": clicks.count(),
        "device_stats": clicks.values("device_type").annotate(count=models.Count("id")),
        "browser_stats": clicks.values("browser").annotate(count=models.Count("id")),
        "os_stats": clicks.values("os").annotate(count=models.Count("id")),
        "clicks_page": clicks_page,
    }

    return render(
        request,
        "links/analytics.html",
        context
    )

@login_required
def toggle_url(request, pk):
    if request.method == "POST":
        short_url = get_object_or_404(ShortURL, id=pk, user=request.user)
        short_url.is_active = not short_url.is_active
        short_url.save()
    return redirect("links:dashboard")

@login_required
def delete_url(request, pk):
    if request.method == "POST":
        short_url = get_object_or_404(ShortURL, id=pk, user=request.user)
        short_url.delete()
    return redirect("links:dashboard")


def rate_limited_view(request, exception=None):
    if isinstance(exception, Ratelimited):
        return render(request, "links/rate_limited.html", status=429)
    return render(request, "links/403.html", status=403)