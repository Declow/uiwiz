from fastapi import Request
from pydantic import BaseModel
from uiwiz.app import UiwizApp
from uiwiz.login_response import LoginResponse
import uiwiz.ui as ui
from uiwiz.request_middelware import get_request
import uvicorn
from datetime import datetime, timezone, timedelta
from starlette.authentication import requires
from starlette.authentication import AuthCredentials, AuthenticationBackend, SimpleUser
from starlette.middleware.authentication import AuthenticationMiddleware

auth_header = "sometokenheader"
# if auth header is included and the server responses with this header
# then it is included in every request going forward when using
# xhr in the browser. This is for API calls
app = UiwizApp(theme="light", auth_header=auth_header)

_COOKIE_ID = "uiwizSession"


# For page auth you will need to implement your own
# AuthenticationBackend class
class BasicAuth(AuthenticationBackend):
    async def authenticate(self, conn):
        if _COOKIE_ID not in conn.cookies:
            return

        auth = conn.cookies[_COOKIE_ID]
        # TODO: You'd want to verify the token/session id before returning
        # The AuthCredentials with the list of scopes on the user is used in
        # the @requires("authenticated") decorator.
        return AuthCredentials(["authenticated", "admin"]), SimpleUser("user")


# Register your auth backend
app.add_middleware(AuthenticationMiddleware, backend=BasicAuth())


def extend_menu(request: Request):
    # Check if the user is aithenticated
    if request.user.is_authenticated:
        with ui.element("li"):
            ui.link("Secret", "/requirelogin")


def create_nav():
    with ui.nav().classes():
        with ui.element("ul").classes("menu menu-horizontal menu-md"):
            with ui.element("li"):
                ui.link("Home", "/")
            with ui.element("li"):
                ui.link("Login", "/login")
            with ui.element("li"):
                ui.themeSelector()
            extend_menu(get_request())


class LoginModel(BaseModel):
    username: str
    password: str


@app.ui("/login/post")
def api_login(model: LoginModel):
    # Replace this with your backend calls to verify the user
    # and create somekind of token or session id
    if model.username == "admin" and model.password == "pass":
        # Set expire time on the cookie
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        response = LoginResponse()
        response.set_token(_COOKIE_ID, "sometokenthatissecure", expire)

        return response

    ui.toast("Bad username or password").error()


@app.ui("/logout/post")
def api_logout():
    expire = datetime.now(timezone.utc) + timedelta(days=-30)
    response = LoginResponse()
    # Expire the cookie on logout
    response.set_token(_COOKIE_ID, "sometokenthatissecure", expire)

    return response


@app.page("/login")
def login():
    create_nav()
    with ui.form().on_submit(api_login):
        ui.input("username", "username")
        ui.input("password", "password")
        with ui.row():
            ui.button("Login")
    with ui.col():
        ui.button("Logout").on_click(api_logout)


# Require the user to have the admin scope
# otherwise redirect to the function login above
@app.page("/requirelogin")
@requires(["admin"], redirect="login")
def secret_page(request: Request):
    create_nav()
    ui.label("secret")


@app.page("/")
async def homepage(request: Request):
    create_nav()
    with ui.element().classes("col"):
        ui.label(f"User is logged in: {request.user.is_authenticated}")
        i = ui.input("test", "name")
        ui.label().bind_text_from(i)

    with ui.footer():
        ui.label("some footer text")


if __name__ == "__main__":
    uvicorn.run("login:app", reload=True)
