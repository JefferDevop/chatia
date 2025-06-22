# admin.py
from django.contrib import admin
from .models import WhatsAppClient, WhatsAppMessage, WhatsAppAgent, WhatsAppConversation, WhatsAppConversationAgent

@admin.register(WhatsAppClient)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('wa_id', 'nombre')

@admin.register(WhatsAppMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ( 'conversacion', 'tipo', 'timestamp', 'mensaje', 'tiempo_respuesta', 'visto')

@admin.register(WhatsAppAgent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'disponible', 'email')


@admin.register(WhatsAppConversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ( 'cliente', 'inicio_conversacion', 'fin_conversacion', 'estado')



@admin.register(WhatsAppConversationAgent)
class ConversationAgentAdmin(admin.ModelAdmin):
    list_display = (  'conversacion', 'agente', 'asignado_en', 'activo')






# # app_whatsapp/admin.py

# from django.contrib import admin
# from .models import WhatsAppMessage, MessageStatus

# @admin.register(WhatsAppMessage)
# class WhatsAppMessageAdmin(admin.ModelAdmin):
#     list_display = ('sender_name', 'wa_id', 'short_body', 'wa_timestamp', 'created_at')
#     search_fields = ('sender_name', 'wa_id', 'message_body')
#     list_filter = ('created_at',)
#     ordering = ('-created_at',)

#     def short_body(self, obj):
#         return (obj.message_body[:50] + '...') if len(obj.message_body) > 50 else obj.message_body
#     short_body.short_description = 'Mensaje'


# @admin.register(MessageStatus)
# class MessageStatusAdmin(admin.ModelAdmin):
#     list_display = ('message_id', 'status', 'recipient_id', 'wa_timestamp', 'created_at')
#     search_fields = ('message_id', 'recipient_id', 'status')
#     list_filter = ('status', 'created_at')
#     ordering = ('-created_at',)
