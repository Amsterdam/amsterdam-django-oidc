import time
from typing import Optional

from django.core.exceptions import PermissionDenied
from mozilla_django_oidc.auth import (
    OIDCAuthenticationBackend as MozillaOIDCAuthenticationBackend,
)


class OIDCAuthenticationBackend(MozillaOIDCAuthenticationBackend):
    def validate_issuer(self, payload: dict[str, str]) -> None:
        issuer = self.get_settings("OIDC_OP_ISSUER")
        iss = payload.get("iss")
        if issuer != iss:
            raise PermissionDenied(
                f'"iss": {iss} does not match configured value for OIDC_OP_ISSUER: {issuer}'
            )

    def validate_audience(self, payload: dict[str, str]) -> None:
        trusted_audiences = self.get_settings("OIDC_TRUSTED_AUDIENCES", [])
        trusted_audiences = set(trusted_audiences)
        audience = payload.get("aud")
        audience = set(audience)
        distrusted_audiences = audience.difference(trusted_audiences)
        if distrusted_audiences:
            raise PermissionDenied(
                f'"aud" contains distrusted audiences: {distrusted_audiences}'
            )

    def validate_expiry(self, payload: dict[str, str]) -> None:
        expire_time = payload.get("exp")
        now = time.time()
        if now > expire_time:
            raise PermissionDenied(
                "Access-token is expired %r > %r" % (now, expire_time)
            )

    def validate_access_token(self, payload: dict[str, str]) -> None:
        self.validate_issuer(payload)
        self.validate_audience(payload)
        self.validate_expiry(payload)

    def get_userinfo(
        self,
        access_token: str,
        id_token: Optional[str] = None,
        payload: Optional[dict[str, str]] = None,
    ) -> dict[str, str]:
        userinfo = self.verify_token(access_token)
        self.validate_access_token(userinfo)

        return userinfo
