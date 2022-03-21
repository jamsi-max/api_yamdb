from rest_framework import serializers

from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    def check_review_exist_from_author(self, data):
        if self.context.get("request").user != "POST":
            return data
        user = self.context.get("request").user
        
            raise ValidationError("Нельзя подписаться на самого себя")
        return value

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review
