# events/admin.py

from django.contrib import admin
from .models import  Donation,  HelpAlert 



admin.site.register(Donation)
admin.site.register(HelpAlert)

from django.contrib.sites.models import Site
site = Site.objects.get_current()
site.domain = 'localhost:8000'  # or your actual domain
site.name = 'Communion'
site.save()

