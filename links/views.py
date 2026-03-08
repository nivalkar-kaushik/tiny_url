from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from ipware import get_client_ip
from user_agents import parse
from .models import ShortURL, ClickAnalytics
from django.db import models


def home(request):
    return render(request, "links/home.html")


def create_short_url(request):
    original_url = request.POST.get("original_url")

    if request.user.is_authenticated:
        # Logged-in user: ignore session
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

def redirect_short_url(request, code):
    short_url = get_object_or_404(ShortURL, code=code, is_active=True)

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