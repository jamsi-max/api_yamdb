from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


from .serializers import SignupSerializer

User = get_user_model()


class SignupView(mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        message = {'info': 'Код потверждения отправлен на электронную почту!'}
        headers = None
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username, email=email).first()

        if user is None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            message = serializer.data
            headers = self.get_success_headers(serializer.data)

        comfirm_token = RefreshToken.for_user(user)

        send_mail('Подтверждение регистрации на Yambd',
                  f'Ваш код подтверждения {comfirm_token}',
                  'yambd@yambd.com',
                  [user.email, ],
                  fail_silently=False)

        return Response(message,
                        status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
