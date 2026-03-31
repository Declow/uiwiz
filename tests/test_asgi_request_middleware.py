import pytest

from uiwiz.middleware.asgi_request_middleware import get_request


def test_get_request_raises_outside_request_context() -> None:
    with pytest.raises(RuntimeError, match="Request context is not available"):
        get_request()
