from rest_framework import serializers
from .models import *

class MenuSelializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'opcion',
            'descripcion',
            )