from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Blog


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        user = User.objects.filter(username = data['username'])
        if user.exists():
            raise serializers.ValidationError('Username is already taken.')
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'].lower(),
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data['username'])
        if not user.exists():
            raise serializers.ValidationError('Account not found.')
        return data
    
    def get_jwt_token(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            return {'message':'Logged in successfully.', 'data':{'token':{'refresh':str(refresh), 'access':str(refresh.access_token)}}}
        else:
            return {'message':'Invalid credentials.', 'data':{}}
        

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['user', 'createdAt', 'updatedAt']