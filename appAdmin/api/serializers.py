from rest_framework import serializers
from ..models import Client, Agent, Conversation, ConversationAgent, MensajeWhatsApp
from accounts.models import Account  # Ajusta si tu modelo está en otro lado

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'nombre', 'wa_id']

class AgentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=Account.objects.all())

    class Meta:
        model = Agent
        fields = ['id', 'user_id', 'nombre', 'email', 'available']

class ConversationAgentSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()

    class Meta:
        model = ConversationAgent
        fields = ['id', 'agent', 'asignado_en', 'activo']

class MensajeWhatsAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeWhatsApp
        fields = [
            'id',
            'conversacion',
            'tipo',
            'mensaje',
            'timestamp',
            'visto',
            'tiempo_respuesta'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    cliente = ClientSerializer()
    agentes = AgentSerializer(many=True)
    mensajes = MensajeWhatsAppSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'cliente',
            'agentes',
            'inicio_conversacion',
            'fin_conversacion',
            'estado',
            'mensajes'
        ]
