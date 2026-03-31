from unittest import mock

from uiwiz import ui


def test_theme_selector_script_uses_samesite_cookie_and_no_console_log() -> None:
    mocked_request = mock.MagicMock()
    mocked_request.cookies = {}

    with mock.patch("uiwiz.elements.theme_selector.get_request", return_value=mocked_request):
        selector = ui.themeSelector()

    assert "SameSite=Lax" in selector.script
    assert "console.log" not in selector.script
