from fastapi.testclient import TestClient

from uiwiz import ui
from uiwiz.app import UiwizApp
from uiwiz.frame import Frame


def test_page_request_exception_cleans_frame_stack() -> None:
    app = UiwizApp()

    @app.page("/boom")
    def boom() -> None:
        ui.label("before")
        raise RuntimeError("boom")

    baseline_stack_ids = set(Frame.stacks.keys())
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/boom")
    status_code = 500
    assert response.status_code == status_code
    assert set(Frame.stacks.keys()) == baseline_stack_ids


def test_ui_request_exception_cleans_frame_stack() -> None:
    app = UiwizApp()

    @app.ui("/boom-ui")
    def boom_ui() -> None:
        ui.label("before")
        raise RuntimeError("boom-ui")

    baseline_stack_ids = set(Frame.stacks.keys())
    client = TestClient(app, raise_server_exceptions=False)
    response = client.post("/boom-ui")
    status_code = 500
    assert response.status_code == status_code
    assert set(Frame.stacks.keys()) == baseline_stack_ids
