from django.urls import path
from . import views

app_name = 'links'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_short_url, name='create_short_url'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<str:code>/', views.redirect_short_url, name='redirect_short_url'),
    path('analytics/<int:pk>/', views.shorturl_analytics, name='analytics'),
]
