from fastapi.testclient import TestClient

from uiwiz import ui
from uiwiz.app import UiwizApp


def test_page_definition_renders_expected_shell_bits() -> None:
    app = UiwizApp(title="My App", theme="light")

    @app.page("/")
    def home() -> None:
        ui.label("hello")

    client = TestClient(app)
    response = client.get("/")
    body = response.text
    status_code = 200
    assert response.status_code == status_code
    assert "<!DOCTYPE html>" in body
    assert 'data-theme="light"' in body
    assert "<title" in body
    assert "My App" in body
    assert "hx-toast-delay" in body


def test_page_definition_prefers_cookie_theme() -> None:
    app = UiwizApp(theme="light")

    @app.page("/")
    def home() -> None:
        ui.label("hello")

    client = TestClient(app)
    client.cookies.set("data-theme", "forest")
    response = client.get("/")
    status_code = 200
    assert response.status_code == status_code
    assert 'data-theme="forest"' in response.text
