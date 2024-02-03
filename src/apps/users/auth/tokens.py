from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


def create_jwt_pair_for_user(user):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

    return tokens

class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.is_active) + str(user.pk) + str(timestamp)
        )


