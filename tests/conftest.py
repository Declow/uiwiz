from unittest import mock

import pytest

from uiwiz import UiwizApp
from uiwiz.frame import Frame
from uiwiz.middleware.asgi_request_middleware import get_request  # noqa: F401
from uiwiz.shared import reset_resources


@pytest.fixture(autouse=True)
def setup_app() -> UiwizApp:
    app = UiwizApp()

    with mock.patch("uiwiz.frame.get_request") as api_mock:
        mo = mock.MagicMock()
        api_mock.return_value = mo
        mo.app = app
        mo.headers = {"hx-target": "a-1"}
        Frame.get_stack()
        reset_resources()
        yield app
        Frame.get_stack().del_stack()
        reset_resources()
