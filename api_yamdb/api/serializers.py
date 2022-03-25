import datetime as dt
import re

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title

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
        read_only_fields = ("role", "is_staff", "is_superuser")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Ошибка! Имя "me" использовать запрещено!'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:

        fields = ("username", "confirmation_code")

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise NotFound(detail="Пользователь не существует", code=404)

        return value

    def validate(self, data):
        try:

            payload = RefreshToken(data.get("confirmation_code"))
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
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Пользователь с таким именем уже существует.",
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Пользователь с таким почтовым ящиком уже существует.",
            )
        ]
    )

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
    slug = serializers.SlugField(
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message="Такой slug уже существует",
            ),
            RegexValidator(
                re.compile(r"^[-a-zA-Z0-9_]+$"),
                message="Slug может содержать латинские буквы, цифры и знак _",
            ),
        ]
    )

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

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
        read_only_fields = fields

    def get_rating(self, obj):
        queryset = Review.objects.filter(title_id=obj.id)
        return queryset.aggregate(Avg("score")).get("score__avg")


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError("Проверьте год произведения!")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
