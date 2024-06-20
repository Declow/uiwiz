from unittest import mock

import pytest

from uiwiz import UiwizApp, element
from uiwiz.asgi_request_middelware import get_request


@pytest.fixture(autouse=True, scope="function")
def setup_app():
    app = UiwizApp()

    with mock.patch("uiwiz.frame.get_request") as api_mock:
        mo = mock.MagicMock()
        api_mock.return_value = mo
        mo.app = app
        mo.headers = {"hx-target": "a-1"}
        element.Frame.del_stack()
        yield api_mock
        element.Frame.del_stack()
