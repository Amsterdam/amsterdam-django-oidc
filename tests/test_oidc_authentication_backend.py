from time import time
from unittest.mock import Mock

import pytest
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.test import TestCase, override_settings

from amsterdam_django_oidc import OIDCAuthenticationBackend


@override_settings(
    OIDC_OP_ISSUER="http://localhost:8002/realms/my-realm",
    OIDC_TRUSTED_AUDIENCES=["me", "you"],
)
class TestOIDCAuthenticationBackend(TestCase):
    _authentication_backend: OIDCAuthenticationBackend

    def setUp(self) -> None:
        self._authentication_backend = OIDCAuthenticationBackend()

    def test_validate_valid_issuer(self) -> None:
        self._authentication_backend.validate_issuer({"iss": "http://localhost:8002/realms/my-realm"})  # type: ignore

    def test_validate_invalid_issuer(self) -> None:
        with pytest.raises(PermissionDenied):
            self._authentication_backend.validate_issuer({"iss": "http://localhost:8002/realms/my-other-realm"})  # type: ignore

    def test_validate_valid_single_audience(self) -> None:
        self._authentication_backend.validate_audience({"aud": "me"})  # type: ignore

    def test_validate_invalid_single_audience(self) -> None:
        with pytest.raises(PermissionDenied):
            self._authentication_backend.validate_audience({"aud": "someone else"})  # type: ignore

    def test_validate_valid_multiple_audiences(self) -> None:
        self._authentication_backend.validate_audience({"aud": ["me", "you"]})  # type: ignore

    def test_validate_partially_valid_multiple_audiences(self) -> None:
        self._authentication_backend.validate_audience({"aud": ["someone else", "you"]})  # type: ignore

    def test_validate_invalid_multiple_audiences(self) -> None:
        with pytest.raises(PermissionDenied):
            self._authentication_backend.validate_audience({"aud": ["someone else", "somebody"]})  # type: ignore

    def test_validate_missing_audience(self) -> None:
        with pytest.raises(SuspiciousOperation):
            self._authentication_backend.validate_audience({})  # type: ignore

    def test_validate_valid_expiry(self) -> None:
        hour_from_now = int(time()) + 3600
        self._authentication_backend.validate_expiry({"exp": hour_from_now})  # type: ignore

    def test_validate_invalid_expiry(self) -> None:
        hour_ago = int(time()) - 3600
        with pytest.raises(PermissionDenied):
            self._authentication_backend.validate_expiry({"exp": hour_ago})  # type: ignore

    def test_validate_missing_expiry(self) -> None:
        with pytest.raises(SuspiciousOperation):
            self._authentication_backend.validate_expiry({})  # type: ignore

    def test_validate_access_token(self) -> None:
        self._authentication_backend.validate_issuer = Mock()  # type: ignore
        self._authentication_backend.validate_audience = Mock()  # type: ignore
        self._authentication_backend.validate_expiry = Mock()  # type: ignore
        payload = {}  # type: ignore

        self._authentication_backend.validate_access_token(payload)  # type: ignore

        self._authentication_backend.validate_issuer.assert_called_once_with(payload)
        self._authentication_backend.validate_audience.assert_called_once_with(payload)
        self._authentication_backend.validate_expiry.assert_called_once_with(payload)

    def test_get_userinfo(self) -> None:
        access_token = "access_token"
        payload = {
            "exp": 1738142309,
            "iat": 1738142009,
            "auth_time": 1738142009,
            "jti": "e5a4f4e4-86e2-4f3b-b723-30a9f8f2b25b",
            "iss": "http://localhost:8002/realms/my-realm",
            "aud": "account",
            "sub": "6277c66b-60be-4073-aeac-12a38890bb4e",
            "typ": "Bearer",
            "azp": "hello",
            "session_state": "cf7fac46-c444-4edb-af24-c5d4cb4b40f1",
            "acr": "1",
            "allowed-origins": ["*"],
            "scope": "email profile",
            "sid": "cf7fac46-c444-4edb-af24-c5d4cb4b40f1",
            "email_verified": True,
            "name": "User",
            "preferred_username": "user",
            "given_name": "User",
            "family_name": "Example",
            "email": "user@example.com",
        }

        self._authentication_backend.verify_token = Mock()  # type: ignore
        self._authentication_backend.verify_token.return_value = payload
        self._authentication_backend.validate_access_token = Mock()  # type: ignore

        self._authentication_backend.get_userinfo(access_token)

        self._authentication_backend.verify_token.assert_called_once_with(access_token)
        self._authentication_backend.validate_access_token.assert_called_once_with(
            payload
        )
