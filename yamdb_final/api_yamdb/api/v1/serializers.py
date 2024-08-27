import datetime as dt

from rest_framework import serializers, validators

from titles.models import Category, Genre, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для юзера"""

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User


class SendCodeSerializer(serializers.ModelSerializer):
    """Сериалайзер для отправки кода подтверждения"""

    email = serializers.EmailField(
        required=True,
        validators=[
            # проверяем чтоб почта не была закреплена за другим юзером
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Данная почта уже занята, укажите пожалуйста другую')]

    )

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True,
        validators=[
            # проверяем чтоб логин не был закреплен за другим юзером
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Такой логин уже занят,укажите пожалуйста другой')]
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя выбрать  себя, выберите другого юзера')
        return value


class CheckCodeSerializer(serializers.Serializer):
    """Сериалайзер для проверки кода подтверждения и генерации токена"""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150
    )
    confirmation_code = serializers.CharField(required=True)


class MeSerializer(serializers.ModelSerializer):
    """Сериалайзер получения профиля юзера"""

    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """Сериалайзер только для чтения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        fields = [
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre',
            'rating'
        ]
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre'
        )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (1000 < value <= year):
            raise serializers.ValidationError(
                'Год не может быть больше текущего'
            )
        return value
