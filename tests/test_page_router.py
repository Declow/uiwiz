from fastapi.routing import APIRoute

from uiwiz.app import UiwizApp
from uiwiz.page_route import PageRouter, Path


def test_page_router_page():
    pr = PageRouter()
    route = "/path"

    @pr.page(route)
    def func():
        ...  # pragma: no cover

    expected_output: Path = {"args": (), "kwargs": {}, "func": func, "type": "page"}

    assert expected_output == pr.paths.get(route)


def test_page_router_ui():
    pr = PageRouter()
    route = "/path"

    @pr.ui(route)
    def func():
        ...  # pragma: no cover

    expected_output: Path = {"args": (), "kwargs": {}, "func": func, "type": "ui"}

    assert expected_output == pr.paths.get(route)


def test_page_go_to_get_request():
    pr = PageRouter()
    route = "/path"

    @pr.page(route)
    def func():
        ...  # pragma: no cover

    app = UiwizApp()
    app.add_page_router(pr)

    apis = {item.path: item for item in app.routes}

    print(apis)

    assert route == app.app_paths[func]
    assert route == apis.get(route).path
    assert "func" == apis.get(route).name
    assert {"GET"} == apis.get(route).methods


def test_ui_go_to_post_request():
    pr = PageRouter()
    route = "/path"

    @pr.ui(route)
    def func():
        ...  # pragma: no cover

    app = UiwizApp()
    app.add_page_router(pr)

    apis = {item.path: item for item in app.routes}

    print(apis)

    assert route == app.app_paths[func]
    assert route == apis.get(route).path
    assert "func" == apis.get(route).name
    assert {"POST"} == apis.get(route).methods
