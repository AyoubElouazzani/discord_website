from rest_framework import serializers
from base.models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'  # Includes all fields in the model
