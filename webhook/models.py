# models.py
from django.db import models

class WhatsAppMessage(models.Model):
    wa_id = models.CharField(max_length=50)
    sender_name = models.CharField(max_length=255)
    message_body = models.TextField()
    wa_timestamp = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {self.sender_name}: {self.message_body[:50]}"


class MessageStatus(models.Model):
    message_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)  # e.g., delivered, read
    recipient_id = models.CharField(max_length=50)
    wa_timestamp = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status.upper()} for {self.recipient_id} at {self.created_at.strftime('%H:%M:%S')}"




# # app_whatsapp/models.py
# from django.db import models

# class WhatsAppMessage(models.Model):
#     wa_id = models.CharField(max_length=50)
#     sender_name = models.CharField(max_length=255)
#     message_body = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender_name}: {self.message_body[:30]}"
