# features/partnerships.py
from django.db import models

class Partnership(models.Model):
    organization_name = models.CharField(max_length=200)
    collaboration_type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.organization_name

def get_partnerships():
    return Partnership.objects.all()
