from rest_framework import serializers
from accounts.models import Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'phone_number', 'username', 'email', 'first_name',
                  'last_name', 'password', 'is_active', 'is_staff']
