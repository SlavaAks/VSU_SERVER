from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create the logging file handler
fh = logging.FileHandler("user.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add handler to logger object
logger.addHandler(fh)



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            f"{user.pk}{timestamp}{user.is_active}"
        )


account_activation_token = TokenGenerator()


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(request.data)
        current_site = get_current_site(request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        print(to_email)
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        try:
            send_mail(mail_subject,
                  message,
                  'aks8slava@mail.ru',
                  [to_email])
        except:
            logger.error("письмо не отправлено")
        finally:

            return Response(status=status.HTTP_201_CREATED)

    def patch(self,request):

        logger.info("Program started")
        # print(request.data.dict())
        print("ss")
        print(request.data)
        user_data = request.data.dict()
        print(user_data)
        logger.info(f'{user_data}')
        # print(user_data["avatar"])

        serializer = UserSerializer(data=user_data,partial=True)
        # print(user_data["avatar"])
        user=serializer.update(request, user_data)
        user=UserSerializer(user)
        print(user.data)
        return Response(user.data,status=status.HTTP_200_OK)

def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')





