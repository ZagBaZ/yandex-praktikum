
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)

from .mixins import MainApiMixViewSet
from .pagination import ApiPagination
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadOnlySerializer,
    SendCodeSerializer,
    CheckCodeSerializer,
    UserSerializer,
    MeSerializer
)
from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAdminOrUserReadOnly)

from titles.models import Category, Genre, Title
from users.models import User
from api_yamdb.settings import CONTACT_EMAIL


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    mail_subject = f'Код подтверждения для {username}'
    adress = [email]
    # добавил created, брал пример из документации
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#get-or-create
    # теперь мы вытягиваем не первый результат из кортежа(было user[0])
    # а просто результат при СОЗДАНИИ
    # раньше тянули в ЛЮБОМ случае (даже если логин уже есть в системе)
    # теперь же лишь тогда когда объект был создан
    user, created = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = (f'Ваш {mail_subject}: {confirmation_code}. \n'
               f'Пожалуйста введите его для получения токена.')
    send_mail(mail_subject, message, CONTACT_EMAIL, adress)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_token(request):
    serializer = CheckCodeSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, code):
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response(
        {'token': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminOrUserReadOnly,
    ]
    lookup_field = 'username'
    search_fields = [
        'username',
    ]

    @action(methods=['patch', 'get'],
            permission_classes=[IsAuthenticated],
            detail=False,
            url_path='me',
            url_name='me',)
    def me(self, request):
        user = self.request.user
        serializer = MeSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(),
        if self.request.method != 'PATCH':
            serializer = MeSerializer(user)
        return Response(serializer.data)


class GenreViewSet(MainApiMixViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        IsAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = ApiPagination


class CategoryViewSet(MainApiMixViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = ApiPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    pagination_class = ApiPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return TitleWriteSerializer
        return TitleReadOnlySerializer
