from unittest import mock

from uiwiz import ui
from uiwiz.frame import Frame


def test_element_html():
    output = str(ui.element())
    assert '<div id="a-0"></div>' == output


def test_element_html_nested_random():
    output = ""
    with ui.element() as root:
        ui.element()
        output = str(root)
    assert '<div id="a-0"><div id="a-1"></div></div>' == output


def test_element_void():
    output = str(ui.element("img"))
    assert '<img id="a-0">' == output


def test_get_target_none():
    el = ui.element()
    assert "this" == el.get_target(None)


def test_get_target_lambda():
    el = ui.element()
    assert "#this" == el.get_target(lambda: "this")


def test_get_target_str():
    el = ui.element()
    assert "#outerHTML" == el.get_target("outerHTML")
    assert "#asd" == el.get_target("asd")
    assert "this" == el.get_target("this")
    assert "#shouldbeok" == el.get_target("#shouldbeok")


def test_get_target_element_id():
    el = ui.element()
    el2 = ui.element()
    assert f"#{el2.id}" == el.get_target(el2)


def test_oob_top_level():
    with ui.element() as root:
        ui.toast("uiwiz")
    assert (
        '<div id="a-0"></div><div id="toast" hx-swap-oob="afterbegin"><div id="a-2" class="alert w-full z-50  relative pr-16" hx-toast-data="{&quot;autoClose&quot;: true}" hx-toast-delete-button=""><span id="a-3">uiwiz</span></div></div>'
        == str(root)
    )


def test_event():
    func = lambda: ui.toast("test")
    html = str(ui.button("Click me").on_click(func))

    assert (
        f'<button id="a-0" class="btn btn-md" hx-target="this" hx-swap="outerHTML" hx-post="/_uiwiz/hash/{func.__hash__()}" hx-trigger="click" hx-ext="json-enc">Click me</button>'
        == html
    )


def test_before_render_lifecycle():
    el = ui.element()
    mo = mock.MagicMock()
    el.before_render = mo

    str(el)

    mo.assert_called_once()


def test_element_get_name():
    el = ui.element()
    assert el.name is None


def test_element_get_value():
    el = ui.element()
    assert el.value is None


def test_element_set_value():
    el = ui.element()
    el.value = "test"
    assert el.value == "test"


def test_element_get_classes():
    el = ui.element().classes("glass")
    assert el.get_classes() == "glass"


def test_add_script():
    script = 'console.log("test")'
    el = ui.element()
    el.script = script
    str(el)
    assert Frame.get_stack().scripts[0] == script


def test_oob_no_render():
    el = ui.element(oob=True)
    assert el.render_self(False) == ""


def test_str_html_escape():
    el = ui.element()
    el.attributes["value"] = "<script>alert('test')</script>"
    assert str(el) == '<div id="a-0" value="&lt;script&gt;alert(&#x27;test&#x27;)&lt;/script&gt;"></div>'


def test_bool_html_escape():
    el = ui.element()
    el.attributes["value"] = True
    assert str(el) == '<div id="a-0" value="true"></div>'


def test_number_html_escape():
    el = ui.element()
    el.attributes["value"] = 123
    assert str(el) == '<div id="a-0" value="123"></div>'


def test_none_html_escape():
    el = ui.element()
    el.attributes["value"] = None
    assert str(el) == '<div id="a-0" value="None"></div>'
