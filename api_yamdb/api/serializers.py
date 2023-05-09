from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'username'
        )
        extra_kwargs = {
            'username': {
                'validators': [
                    UniqueValidator(queryset=User.objects.all())
                ]
            }
        }


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
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

