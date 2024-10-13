# features/feedback.py
from django.db import models

class Feedback(models.Model):
    user_id = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from user {self.user_id}"

def get_feedback():
    return Feedback.objects.all()
