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
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username, email=email).first()

        if not user:
            respons = super().create(request, *args, **kwargs)
            return respons

        comfirm_token = RefreshToken.for_user(user)

        send_mail('Token comfirm',
                  f'You token comfirm is {comfirm_token}',
                  'yambd@yambd.com',
                  [user.email, ],
                  fail_silently=False)

        return Response(
            {'info': 'The confirmation key has been sent to your email'},
            status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user = serializer.save()
        comfirm_token = RefreshToken.for_user(user)

        send_mail('Token comfirm',
                  f'You token comfirm is {comfirm_token}',
                  'yambd@yambd.com',
                  [user.email, ],
                  fail_silently=False)
