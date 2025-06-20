# models.py
from django.db import models
from django.utils import timezone

class WhatsAppContact(models.Model):
    wa_id = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    last_interaction = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre or ''} ({self.wa_id})"
    

class WhatsAppMessage(models.Model):
    wa_id = models.CharField(max_length=50)
    sender_name = models.CharField(max_length=100, blank=True)
    message_body = models.TextField()
    wa_timestamp = models.CharField(max_length=20)
    message_type = models.CharField(max_length=10, default="unassigned")  # 'received' o 'sent'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {self.sender_name}: {self.message_body[:50]}"


class WhatsAppMessageStatus(models.Model):
    message_id = models.CharField(max_length=100)  # ID de WhatsApp
    wa_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20)  # delivered, read, etc.
    timestamp = models.DateTimeField(default=timezone.now)
    conversation_id = models.CharField(max_length=100, blank=True, null=True)
    pricing_model = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status.upper()} for {self.message_id} at {self.created_at.strftime('%H:%M:%S')}"




# # app_whatsapp/models.py
# from django.db import models

# class WhatsAppMessage(models.Model):
#     wa_id = models.CharField(max_length=50)
#     sender_name = models.CharField(max_length=255)
#     message_body = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender_name}: {self.message_body[:30]}"
