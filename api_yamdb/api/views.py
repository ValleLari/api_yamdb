from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .permissions import (IsAdmin)
from .serializers import (RegisterSerializer, TokenSerializer,
                          UserEditSerializer, UserSerializer)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
            detail=False,
            serializer_class=UserEditSerializer,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me')
    def user_self_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на yamdb',
        message=f'Ваш код доступа: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
