from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = None
        if header is not None:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        try:
            validated = self.get_validated_token(raw_token)
            user = self.get_user(validated)
        except Exception as exc:
            raise exceptions.AuthenticationFailed(str(exc))

        return (user, validated)
