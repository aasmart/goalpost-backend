from django.shortcuts import render
from rest_framework import viewsets, permissions
from goalpost_app.models import GoalpostUser, Goal, GoalReflection
from goalpost_app.serializers import UserSerializer, GoalSerializer, GoalReflectionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewPermission(permissions.BasePermission):
    """
    Limits the view of all users to admins, while individual
    users are limited to themselves 
    """
    def has_permission(self, request, view):
        if view.action == 'retrieve':
            return True
        else:
            return request.user.is_authenticated and request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff and request.user.is_authenticated) or obj.id == request.user.id

class GoalpostUserViewSet(viewsets.ModelViewSet):
    queryset = GoalpostUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]

class GoalViewPermission(permissions.BasePermission):
    """
    Limits the view of a user's goals to admin users and the
    user themselves
    """
    def has_permission(self, request, view):
        route_user_id = view.kwargs.get("user_pk", None)
        user_id = request.user.id

        try:
            if int(user_id) == int(route_user_id):
                return True
            else:
                return request.user.is_authenticated and request.user.is_admin
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff and request.user.is_authenticated) or obj.user.id == request.user.id
    
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [GoalViewPermission]

    def get_queryset(self):
       return self.queryset.filter(user_id = self.kwargs["user_pk"])
    
class GoalReflectionViewPermission(permissions.BasePermission):
    """
    Limits the viewing of a goall's reflections to admin users or the user
    themselves 
    """
    def has_permission(self, request, view):
        route_user_id = view.kwargs.get("user_pk", None)
        user_id = request.user.id

        try:
            if int(user_id) == int(route_user_id):
                return True
            else:
                return request.user.is_authenticated and request.user.is_admin
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff and request.user.is_authenticated) or obj.user.id == request.user.id
    
class GoalReflectionViewSet(viewsets.ModelViewSet):
    queryset = GoalReflection.objects.all()
    serializer_class = GoalReflectionSerializer
    permission_classes = [GoalReflectionViewPermission]

    def get_queryset(self):
       return self.queryset.filter(goal_id = self.kwargs["goal_pk"])