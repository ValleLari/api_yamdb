from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User

valid_username = UnicodeUsernameValidator()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            valid_username,
        ],
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            valid_username,
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')
        extra_kwargs = {
            'username': {
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }
        }


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            valid_username,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, user):
        if user.lower() == 'me':
            raise serializers.ValidationError(
                'Пользователь me не может быть изменен'
            )
        return user

    def validate(self, data):
        if (
            User.objects.filter(username=data['username']).exists()
            and User.objects.get(username=data['username']).email
            != data['email']
        ):
            raise serializers.ValidationError(
                'Неверна указана почта, или логин уже занят!',
            )
        if (
            User.objects.filter(email=data['email']).exists()
            and User.objects.get(email=data['email']).username
            != data['username']
        ):
            raise serializers.ValidationError('Неверный логин')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review',)
