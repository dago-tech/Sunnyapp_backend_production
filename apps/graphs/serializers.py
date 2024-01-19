from rest_framework import serializers
from .models import DataItem

"""
Serializadores para convertir los modelos de Django en formato JSON
"""

class DataItemSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(input_formats=["%d/%m/%Y"])

    class Meta:
        model = DataItem
        fields = "__all__"

    # Representar la fecha en el formato deseado al retornar el JSON
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['fecha'] = instance.fecha.strftime("%d/%m/%Y")
        return representation