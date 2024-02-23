from datetime import datetime
import typing
from fastapi import Response


class LoginResponse(Response):
    def __init__(
        self,
        url: str = "/",
        headers: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        super().__init__("", 200, headers)
        self.headers["Hx-Redirect"] = url
        self.body = b""

    def set_token(
        self,
        session_id: str,
        session_token: str,
        expires: typing.Union[datetime, str, int],
    ):
        self.set_cookie(
            session_id,
            session_token,
            expires=expires,
            secure=True,
            samesite="strict",
        )
