SECRET_KEY = "fake-key"
USE_TZ = False
ROOT_URLCONF="tests.urls"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "tests",
]
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": ":memory:",
    },
}
OIDC_OP_TOKEN_ENDPOINT = (
    "http://keycloak:8002/realms/my-realm/protocol/openid-connect/token"
)
OIDC_OP_USER_ENDPOINT = (
    "http://keycloak:8002/realms/my-realm/protocol/openid-connect/userinfo"
)
OIDC_RP_CLIENT_ID = "my-client"
OIDC_RP_CLIENT_SECRET = ""
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_JWKS_ENDPOINT = (
    "http://keycloak:8002/realms/my-realm/protocol/openid-connect/certs"
)
OIDC_AUTHENTICATION_CALLBACK_URL = "index"
