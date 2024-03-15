import pytest
from uiwiz import UiwizApp
from unittest import mock


@pytest.fixture(autouse=True, scope="session")
def setup_app():
    app = UiwizApp()

    with mock.patch("uiwiz.element.get_request") as api_mock:
        mo = mock.MagicMock()
        api_mock.return_value = mo
        mo.app = app
        mo.headers = {"hx-target": "a-1"}
        yield api_mock
