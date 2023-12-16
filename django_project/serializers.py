from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.first_name + user.last_name
        return token

from django.contrib.auth.forms import PasswordResetForm
from .forms import SendInviteForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers

###### IMPORT YOUR USER MODEL ######
from accounts.models import CustomUser


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # password_reset_form_class = PasswordResetForm
    password_reset_form_class = SendInviteForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)

        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        ###### FILTER YOUR USER MODEL ######
        if not CustomUser.objects.filter(email=value).exists():

            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            ###### USE YOUR TEXT FILE ######
            'email_template_name': 'registration/password_reset_email.html',
            'html_email_template_name': 'registration/password_reset_email.html',
            'request': request,
        }
        self.reset_form.save(**opts)