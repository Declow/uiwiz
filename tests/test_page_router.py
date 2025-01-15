from uiwiz.app import UiwizApp
from uiwiz.page_route import PageRouter
from uiwiz.shared import fetch_route


def test_page_go_to_get_request():
    pr = PageRouter()
    route = "/path"

    @pr.page(route)
    def func():
        ...  # pragma: no cover

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
    def func():
        ...  # pragma: no cover

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
    def func():
        ...  # pragma: no cover

    apis = {item.path: item for item in app.routes}

    assert route == fetch_route(func)
    assert route == apis.get(route).path
    assert "func" == apis.get(route).name
    assert {"POST"} == apis.get(route).methods
