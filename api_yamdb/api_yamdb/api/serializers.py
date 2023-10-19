from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from .mixins import UserBaseSerializer

User = get_user_model()


class UserSerializer(UserBaseSerializer):
    ...


class UserSignUpSerializer(UserBaseSerializer):
    ...


class TokenSerializer(UserBaseSerializer):
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'rating', 'name', 'year', 'description', 'genre', 'category',
        )

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            average_score = reviews.aggregate(Avg('score'))['score__avg']
            return average_score
        return None

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['category'] = CategorySerializer(instance.category).data
        repr['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        return repr


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ['id', 'author', 'text', 'pub_date', 'score']

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_pk']
        author = self.context['request'].user
        method = self.context['request'].method

        if method == 'POST' and Review.objects.filter(
            author=author, title_id=title_id
        ).exists():
            raise ValidationError(
                'You have already reviewed this title'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
