# features/customized_notifications.py
from django.db import models

class UserNotificationSetting(models.Model):
    user_id = models.IntegerField()
    notification_type = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.notification_type} for user {self.user_id}"

def get_user_settings(user_id):
    return UserNotificationSetting.objects.filter(user_id=user_id)
