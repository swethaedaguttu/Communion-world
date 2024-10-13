"""
URL configuration for community_connect project.

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
# community_connect/urls.py

# community_connect/urls.py

from django.contrib import admin
from django.urls import path, include
from events import views  # Import views from the 'events' app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('communities/', include('events.urls')),
    path('events/', include('events.urls')),
    path('', views.index, name='index'),  # Set the index view for the root URL
    path('login/', views.user_login, name='user_login'),  # Add this for login URL
    path('features/', include('features.urls')),
    path('about/', views.about_us, name='about_us'),  # Add the about us path
    path('contact/', views.contact, name='contact'),  # Add the contact path
    path('profile/', views.profile, name='profile'),  # Ensure this line exists
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
]







