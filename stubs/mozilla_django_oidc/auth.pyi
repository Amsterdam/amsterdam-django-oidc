from typing import Any

from django.contrib.auth.backends import ModelBackend

from amsterdam_django_oidc import Payload

class OIDCAuthenticationBackend(ModelBackend):
    @staticmethod
    def get_settings(attr: str, *args) -> Any: ...
    def verify_token(self, token: str, **kwargs) -> Payload: ...
