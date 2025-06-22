from rest_framework import serializers, viewsets
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.utils import timezone
from django.db import IntegrityError
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
import pytz

from ..models import WhatsAppClient, WhatsAppAgent, WhatsAppConversation, WhatsAppConversationAgent, WhatsAppMessage

# Serializers
class WhatsAppClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppClient
        fields = '__all__'


class WhatsAppAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppAgent
        fields = '__all__'


class WhatsAppConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppConversation
        fields = '__all__'


class WhatsAppConversationAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppConversationAgent
        fields = '__all__'


class WhatsAppMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppMessage
        fields = '__all__'


