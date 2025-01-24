import html

from uiwiz import ui


def test_raw_html():
    html = ui.html("<strong>test</strong>")
    assert '<div id="a-0"><strong>test</strong></div>' == str(html)


def test_escaped_html():
    input = "<strong>test</strong>"
    _html = ui.element(content=input)
    assert f'<div id="a-0">{html.escape(input)}</div>' == str(_html)
