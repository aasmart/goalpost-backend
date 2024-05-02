from django.shortcuts import render
from rest_framework import viewsets, permissions
from goalpost_app.models import GoalpostUser
from goalpost_app.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = GoalpostUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]