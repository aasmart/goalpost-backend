from django.urls import reverse
from goalpost_app.models import GoalpostUser, Goal, GoalReflection
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

class GoalReflectionSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'goal_pk': 'goal__pk',
        'user_pk': 'goal_user__pk',
    }

    class Meta:
        model = GoalReflection
        fields = [
            'id',
            'is_completed', 
            'made_progress', 
            'made_progress_reflection', 
            'could_do_better', 
            'could_do_better_reflection',
            'steps_to_improve'
        ]

class GoalSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'user_pk': 'user__pk',
    }

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'begin_date', 'completion_date', 'accomplished_goal', 'reflections']

    reflections = GoalReflectionSerializer(
        many=True,
        read_only=True
    )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoalpostUser
        fields = ['id', 'email', 'first_name', 'level', 'experience', 'goals']
    
    goals = GoalSerializer(
        many=True,
        read_only=True
    )

class GoalpostUserDetailsSerializer(UserDetailsSerializer):
    """
    Used for displaying info after a user logs in
    """
    class Meta:
        model = GoalpostUser
        fields = ['id', 'email', 'first_name', 'level', 'experience']