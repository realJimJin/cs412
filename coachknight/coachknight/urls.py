"""
URL configuration for coachknight project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    from marketplace.models import CoachProfile, JobPost
    coaches = CoachProfile.objects.filter(actively_looking=True).order_by('-created_at')[:8]
    jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')[:8]
    return render(request, 'home.html', {'coaches': coaches, 'jobs': jobs})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('messaging/', include('messaging.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
