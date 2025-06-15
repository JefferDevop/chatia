
# app_whatsapp/models.py
from django.db import models

class WhatsAppMessage(models.Model):
    wa_id = models.CharField(max_length=50)
    sender_name = models.CharField(max_length=255)
    message_body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_name}: {self.message_body[:30]}"
