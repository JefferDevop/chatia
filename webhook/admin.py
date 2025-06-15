# app_whatsapp/admin.py

from django.contrib import admin
from .models import WhatsAppMessage, MessageStatus

@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'wa_id', 'short_body', 'wa_timestamp', 'created_at')
    search_fields = ('sender_name', 'wa_id', 'message_body')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def short_body(self, obj):
        return (obj.message_body[:50] + '...') if len(obj.message_body) > 50 else obj.message_body
    short_body.short_description = 'Mensaje'


@admin.register(MessageStatus)
class MessageStatusAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'status', 'recipient_id', 'wa_timestamp', 'created_at')
    search_fields = ('message_id', 'recipient_id', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
