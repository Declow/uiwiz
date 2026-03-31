from unittest import mock

from uiwiz import ui


def test_theme_selector_uses_cookie_theme_as_placeholder() -> None:
    mocked_request = mock.MagicMock()
    mocked_request.cookies = {"data-theme": "forest"}

    with mock.patch("uiwiz.elements.theme_selector.get_request", return_value=mocked_request):
        selector = ui.themeSelector()

    html = str(selector.theme_selector)
    assert "forest" in html
