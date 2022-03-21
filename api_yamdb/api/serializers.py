from rest_framework.exceptions import NotFound
import datetime as dt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Пользователь с таким почтовым ящиком уже существует.",
            )
        ]
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Ошибка! Имя "me" использовать запрещено!'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    verify_token = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "verify_token")

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise NotFound(detail="Пользователь не существует", code=404)

        return value

    def validate(self, data):
        try:
            payload = RefreshToken(data.get("verify_token"))
            user_id = payload.get("user_id", None)
        except TokenError:
            raise serializers.ValidationError(
                "Ошибка! Токен не действительный или не существует!"
            )

        user = User.objects.filter(id=user_id).first()
        if user.username != data.get("username"):
            raise serializers.ValidationError(
                "Ошибка! Username не соответствует токену!"
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")

    def validate_slug(self, value):
        # валидация символов?
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False, read_only=True)
    category = CategorySerializer(required=False, read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError("Проверьте год произведения!")
        return value


# class ReviewSerializer(serializers.ModelSerializer):
#    author = serializers.SlugRelatedField(
#        many=False, read_only=True, slug_field="username"
#    )
#
#    def check_review_exist_from_author(self, data):
#        if self.context.get("request").user != "POST":
#            return data
#        user = self.context.get("request").user
#
#            raise ValidationError("Нельзя подписаться на самого себя")
#        return value
#
#    class Meta:
#        fields = ("id", "text", "author", "score", "pub_date")
#         model = Review
