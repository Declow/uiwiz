from uiwiz.login_response import LoginResponse


def test_login_response_sets_htmx_redirect_header() -> None:
    response = LoginResponse(url="/dashboard")
    assert response.headers["Hx-Redirect"] == "/dashboard"


def test_login_response_sets_secure_token_cookie() -> None:
    response = LoginResponse()
    response.set_token("sid", "token", 123)
    cookie_header = response.headers.get("set-cookie", "")
    assert "sid=token" in cookie_header
    assert "HttpOnly" in cookie_header
    assert "SameSite=strict" in cookie_header
