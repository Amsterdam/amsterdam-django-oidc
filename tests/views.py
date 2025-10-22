from django.http import HttpResponse
from django.http.request import HttpRequest


def index(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    return HttpResponse("Hello world!")
