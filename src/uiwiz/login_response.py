from __future__ import annotations

import typing

from fastapi import Response

if typing.TYPE_CHECKING:
    from datetime import datetime


class LoginResponse(Response):
    def __init__(
        self,
        url: str = "/",
        headers: typing.Mapping[str, str] | None = None,
    ) -> None:
        super().__init__("", 200, headers)
        self.headers["Hx-Redirect"] = url
        self.body = b""

    def set_token(
        self,
        session_id: str,
        session_token: str,
        expires: datetime | str | int,
    ) -> None:
        self.set_cookie(session_id, session_token, expires=expires, secure=True, samesite="strict", httponly=True)
