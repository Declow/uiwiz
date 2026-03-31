from fastapi.testclient import TestClient

from uiwiz.app import UiwizApp
from uiwiz.version import __version__


def test_static_middleware_sets_cache_control_for_static_paths() -> None:
    app = UiwizApp(cache_age=120)
    client = TestClient(app)

    response = client.get(f"/_static/{__version__}/app.css")
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "max-age=120"


def test_static_middleware_does_not_match_non_static_path_with_query() -> None:
    app = UiwizApp(cache_age=120)

    @app.get("/probe")
    def probe() -> dict[str, str]:
        return {"ok": "true"}

    client = TestClient(app)
    response = client.get("/probe?src=static/fake.css")
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") is None
