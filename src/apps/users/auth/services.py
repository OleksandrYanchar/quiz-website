# services.py
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import EmailTokenGenerator 


def _send_email(request, user, template, subject):
    current_site = get_current_site(request)
    body = render_to_string(
        template,
        {
            "user": user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': EmailTokenGenerator().make_token(user),
        }
    )
    user.email_user(subject=subject, message=body)

