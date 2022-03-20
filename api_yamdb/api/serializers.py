from lib2to3.pgen2.tokenize import TokenError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким почтовым ящиком уже существует.')]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Ошибка! Имя "me" использовать запрещено!')
        return value


class CustomTokenRefreshSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    verify_token = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'verify_token')

    def validate_username(self, value):
        user = get_object_or_404(User, username=value)
        if user is None:
            raise serializers.ValidationError(
                'Ошибка! Пользователь не существует!')
        return value

    def validate(self, data):
        try:
            payload = RefreshToken(data.get('verify_token'))
            user_id = payload.get('user_id', None)
        except TokenError:
            raise serializers.ValidationError(
                'Ошибка! Токен не действительный или не существует!')

        user = User.objects.filter(id=user_id).first()
        if user.username != data.get('username'):
            raise serializers.ValidationError(
                'Ошибка! Username не соответствует токену!')

        return data
