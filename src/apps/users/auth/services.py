# services.py
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import EmailVerificationTokenGenerator  # Import your token generator
from django.contrib.auth.password_validation import validate_password 
from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError


def _send_email_verification(request, user, template):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    body = render_to_string(
        template,
        {
            "user": user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': EmailVerificationTokenGenerator().make_token(user),
        }
    )
    user.email_user(subject=subject, message=body)

