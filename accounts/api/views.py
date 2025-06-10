from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from accounts.models import Account
from accounts.api.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = Account.objects.all()

    def create(self, request, *args, **kwargs):
        #request.data._mutable = True
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        password = request.data['password']
        if password:
            request.data['password'] = make_password(password)
        else:
            request.data['password'] = request.user.password
        return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
