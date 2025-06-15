# app_whatsapp/admin.py
from django.contrib import admin
from .models import WhatsAppMessage

@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ('wa_id', 'sender_name', 'timestamp')
    search_fields = ('sender_name', 'message_body')
    list_filter = ('timestamp',)