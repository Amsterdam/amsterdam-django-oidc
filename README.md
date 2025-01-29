# amsterdam-django-oidc
This package contains an authentication backend for Django.
It is currently based on the authentication backend provided by Mozilla through the `mozilla-django-oidc` package.
The Mozilla package however does not validate the `iss`, `aud` and `exp` claims of the access token and always calls
the `userinfo` endpoint on the identity provider. Unfortunately that is not adequate for the use case within the 
landscape of applications of the city of Amsterdam. Hence, the reason for this solution.

Instead of calling the `userinfo` endpoint, it will validate the aforementioned claims.

# Install
The package can installed using your favorite package manager for python.
For example using poetry:
```shell
poetry add amsterdam-django-oidc
```

Or using pip:
```shell
pip install amsterdam-django-oidc
```

# Usage
Add the backend to the setting `AUTHENTICATION_BACKENDS`:
```python
# settings.py
AUTHENTICATION_BACKENDS = [
    # ...
    "amsterdam_django_oidc.OIDCAuthenticationBackend",
]
```

There are also a few settings required in addition to those of the Mozilla package:

| Name                   | Type      | Description                                                                                                      |
|------------------------|-----------|------------------------------------------------------------------------------------------------------------------|
| OIDC_OP_ISSUER         | str       | The allowed issuer, the value of the `iss` claim in the access token must match the value of this setting        |
| OIDC_TRUSTED_AUDIENCES | list[str] | Audiences that we trust, at least one of the values of the `aud` claim must match one the values of this setting |
