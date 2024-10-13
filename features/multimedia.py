# features/multimedia.py
from django.db import models

class Media(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def get_all_media():
    return Media.objects.all()
