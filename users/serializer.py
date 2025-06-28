from .models import PQRS
from adminUser.models import TypesPQRS
from rest_framework import serializers

class PQRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PQRS
        fields = '__all__'  # Serializa todos los campos del modelo PQRS
        read_only_fields = ['id', 'created_at', 'updated_at']
        # Puedes especificar campos específicos si no quieres serializar todos
        # fields = ['id', 'name', 'email', 'message']  # Ejemplo de campos específicos
        # read_only_fields = ['id']  # Si quieres que el campo 'id' sea de solo lecjtura
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'message': {'required': True}
        }
        # Puedes agregar validaciones adicionales si es necesario
        # def validate_email(self, value):
        #     if not value.endswith('@example.com'):
        #         raise serializers.ValidationError("El correo electrónico debe ser de example.com")
        #     return value
        # def validate(self, data):
        #     if data['name'] == data['email']:
        #         raise serializers.ValidationError("El nombre y el correo electrónico no pueden ser iguales")
        #     return data


class TypesPQRSApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypesPQRS
        fields = '__all__'  # Serializa todos los campos del modelo TypesPQRS
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
            'timeExecute': {'required': True},
            'area_redirect': {'required': False}
        }
        # Puedes agregar validaciones adicionales si es necesario