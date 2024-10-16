"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import my_data
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), # Admin panel
    path('api/data/', my_data), # Example data view if needed for testing
    path('db/', include('db.urls')),  # Include the db app's URLs
    path('api/', include('db.urls')), # API endpoints, all API-related URLs are routed here
]
