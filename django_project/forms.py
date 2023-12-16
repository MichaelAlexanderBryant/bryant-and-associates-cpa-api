from os import path

from allauth.account.forms import (
    EmailAwarePasswordResetTokenGenerator,
    ResetPasswordForm,
)
from allauth.account.utils import user_pk_to_url_str
from django.conf import settings
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _



class SendInviteForm(ResetPasswordForm):
    """
    used to send an invitation to reset the password
    """

    default_token_generator = EmailAwarePasswordResetTokenGenerator()

    def send_email_invite(self, email, uri, uid, token):
        context = {
            "domain": uri,
            "uid": uid,
            "token": token,
        }
        msg_html = render_to_string("registration/password_reset_email.html", context)
        send_mail(
            "Bryant & Associates CPA - Client Portal - Password Reset",
            None,
            None,
            [email],
            html_message=msg_html,
        )

    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", self.default_token_generator)
        for user in self.users:
            temp_key = token_generator.make_token(user)
            uri = settings.CLIENT_BASE_URL + "/#/reset-password"
            self.send_email_invite(email, uri, user_pk_to_url_str(user), temp_key)
        return self.cleaned_data["email"]
