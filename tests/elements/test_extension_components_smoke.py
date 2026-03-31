from uiwiz import ui
from uiwiz.frame import Frame


def test_markdown_registers_css_extensions() -> None:
    ui.markdown("# hello")
    extensions = Frame.get_stack().extensions
    assert any("Markdown/markdown.css" in item for item in extensions)
    assert any("Markdown/codehighlight.css" in item for item in extensions)


def test_ace_registers_js_extensions() -> None:
    ui.ace(name="editor", content="print('ok')")
    extensions = Frame.get_stack().extensions
    assert any("Ace/ace.min.js" in item for item in extensions)
    assert any("Ace/ace.js" in item for item in extensions)


def test_aggrid_registers_extensions() -> None:
    ui.aggrid(None)
    extensions = Frame.get_stack().extensions
    assert any("Aggrid/aggrid-community.min.js" in item for item in extensions)
    assert any("Aggrid/aggridtheme.css" in item for item in extensions)


def test_echart_registers_extensions() -> None:
    ui.echart({"xAxis": {}, "yAxis": {}, "series": []})
    extensions = Frame.get_stack().extensions
    assert any("EChart/echart.min.js" in item for item in extensions)
    assert any("EChart/echart.js" in item for item in extensions)
