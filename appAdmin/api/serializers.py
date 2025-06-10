from rest_framework import serializers
from accounts.api.serializers import UserSerializer
from ..models import Client, Agent, Message, Conversation, Task, Tag, WebhookEvent
from accounts.models import Account

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ['id', 'username', 'email']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = '__all__'
