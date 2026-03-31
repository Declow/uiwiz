from fastapi.testclient import TestClient
from pydantic import BaseModel

from uiwiz.app import UiwizApp


class UserInput(BaseModel):
    name: str
    age: int


def _create_app() -> UiwizApp:
    app = UiwizApp()

    @app.ui("/submit")
    async def submit(data: UserInput):
        return None

    return app


def test_validation_error_handles_missing_body() -> None:
    client = TestClient(_create_app())
    response = client.post("/submit")
    assert response.status_code == 400
    assert response.headers["x-uiwiz-validation-error"] == "true"


def test_validation_error_handles_field_specific_errors() -> None:
    client = TestClient(_create_app())
    response = client.post("/submit", json={"name": "Jane", "age": "not-an-int"})
    assert response.status_code == 400
    assert response.headers["x-uiwiz-validation-error"] == "true"
    assert "age" in response.text
