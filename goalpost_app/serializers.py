from goalpost_app.models import GoalpostUser
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoalpostUser
        fields = ['url', 'email', 'password']