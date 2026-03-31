from fastapi.testclient import TestClient

from uiwiz import ui
from uiwiz.app import UiwizApp


def test_page_renders_favicon_link_when_provided() -> None:
    app = UiwizApp()

    @app.page("/", favicon="/favicon.ico")
    def home() -> None:
        ui.label("hello")

    client = TestClient(app)
    response = client.get("/")
    status_code = 200
    assert response.status_code == status_code
    assert 'href="/favicon.ico"' in response.text
    assert 'rel="icon"' in response.text
