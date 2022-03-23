from rest_framework import serializers
from .models import Swap

class SwapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swap
        fields = '__all__'