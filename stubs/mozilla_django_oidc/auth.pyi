from typing import Any

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser

from amsterdam_django_oidc import Payload

class OIDCAuthenticationBackend(ModelBackend):
    OIDC_RP_SIGN_ALGO: str
    OIDC_RP_IDP_SIGN_KEY: str | None
    OIDC_RP_CLIENT_SECRET: str

    @staticmethod
    def get_settings(attr: str, *args: Any) -> str | None: ...  # noqa: ANN401
    def verify_token(self, token: str, **kwargs: dict[str, Any]) -> Payload: ...
    def retrieve_matching_jwk(self, token: str) -> str: ...
    def get_payload_data(self, token: str, key: str) -> Payload: ...
    def get_token(self, payload: dict[str, Any]) -> dict[str, Any]: ...
    def filter_users_by_claims(
        self,
        claims: dict[str, Any],
    ) -> list[AbstractBaseUser]: ...
