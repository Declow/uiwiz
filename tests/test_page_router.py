from fastapi.testclient import TestClient

from src import ui
from src.app import UiwizApp
from src.page_route import PageRouter
from src.shared import fetch_route


def test_page_go_to_get_request():
    pr = PageRouter()
    route = "/path"

    @pr.page(route)
    def func(): ...  # pragma: no cover

    app = UiwizApp()
    app.include_router(pr)

    apis = {item.path: item for item in app.routes}

    assert route == fetch_route(func)
    assert route == apis.get(route).path
    assert "func" == apis.get(route).name
    assert {"GET"} == apis.get(route).methods


def test_ui_go_to_post_request():
    app = UiwizApp()

    pr = PageRouter()
    route = "/path"

    @pr.ui(route)
    def func(): ...  # pragma: no cover

    app.include_router(pr)

    apis = {item.path: item for item in app.routes}

    assert route == fetch_route(func)
    assert route == apis.get(route).path
    assert "func" == apis.get(route).name
    assert {"POST"} == apis.get(route).methods


def test_app_ui_go_to_post_request():
    app = UiwizApp()

    route = "/path"

    @app.ui(route)
    def func(): ...  # pragma: no cover

    apis = {item.path: item for item in app.routes}

    assert route == fetch_route(func)
    assert route == apis.get(route).path
    assert "func" == apis.get(route).name
    assert {"POST"} == apis.get(route).methods


def test_router_ui_prefix():
    app = UiwizApp()

    pr = PageRouter(prefix="/api")
    route = "/path"

    @pr.ui(route)
    def func(): ...  # pragma: no cover

    app.include_router(pr)
    apis = {item.path: item for item in app.routes}
    full_route = pr.prefix + route

    assert full_route == fetch_route(func)
    assert full_route == apis.get(full_route).path
    assert "func" == apis.get(full_route).name
    assert {"POST"} == apis.get(full_route).methods


def test_router_page_prefix():
    app = UiwizApp()

    pr = PageRouter(prefix="/page")
    route = "/path"

    @pr.page(route)
    def func(): ...  # pragma: no cover

    app.include_router(pr)
    apis = {item.path: item for item in app.routes}
    full_route = pr.prefix + route

    assert full_route == fetch_route(func)
    assert full_route == apis.get(full_route).path
    assert "func" == apis.get(full_route).name
    assert {"GET"} == apis.get(full_route).methods


def test_router_page_without_prefix():
    app = UiwizApp()

    pr = PageRouter()
    route = "/path"

    @pr.page(route)
    def func(): ...  # pragma: no cover

    app.include_router(pr)
    apis = {item.path: item for item in app.routes}
    full_route = pr.prefix + route

    assert full_route == fetch_route(func)
    assert full_route == apis.get(full_route).path
    assert "func" == apis.get(full_route).name
    assert {"GET"} == apis.get(full_route).methods


def test_router_ui_without_extensions():
    app = UiwizApp()

    pr = PageRouter()
    route = "/path"

    @pr.ui(route, include_js=False, include_css=False)
    def func():
        ui.markdown("""
# Test
## Test
### Test
""")

    app.include_router(pr)

    client = TestClient(app)
    response = client.post(route)
    body = response.read().decode("utf-8")
    assert response.status_code == 200
    assert "Markdown/markdown.css" not in body
    assert "Markdown/codehighlight.css" not in body


def test_router_ui_extensions():
    app = UiwizApp()

    pr = PageRouter()
    route = "/path"

    @pr.ui(route)
    def func():
        ui.markdown("""
# Test
## Test
### Test
""")

    app.include_router(pr)

    client = TestClient(app)
    response = client.post(route)
    body = response.read().decode("utf-8")
    assert response.status_code == 200
    assert "Markdown/markdown.css" not in body
    assert "Markdown/codehighlight.css" not in body
