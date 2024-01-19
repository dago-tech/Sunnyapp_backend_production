from rest_framework import serializers
from .models import CustomUser

"""
Serializadores para convertir los modelos de Django en formato JSON
"""


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        """
        Se sobreescribe el método create para asegurar la validación de password
        """
        # Obtiene y borra la contraseña de la data, si no la encuentra password=None
        password = validated_data.pop("password", None)
        # Crea una nueva instancia con el resto de datos
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
