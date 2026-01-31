from rest_framework import serializers
from django.contrib.auth import get_user_model
from customers.models import Customer

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'phone']

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        name = validated_data.pop('name')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        Customer.objects.create(
            user=user,
            name=name,
            phone=phone,
            email=user.email
        )
        return user
