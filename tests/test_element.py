from uiwiz import ui, element


def test_element_html():
    element.Frame.del_stack()
    output = str(ui.element())

    assert f'<div id="a-0"></div>' == output


def test_element_html_nested_random():
    element.Frame.del_stack()
    output = ""
    with ui.element() as root:
        ui.element()
        output = str(root)
    assert f'<div id="a-0"><div id="a-1"></div></div>' == output


def test_element_void():
    element.Frame.del_stack()
    output = str(ui.element("img"))

    assert f'<img id="a-0">' == output


def test_get_target_none():
    element.Frame.del_stack()
    el = ui.element()
    assert "this" == el.get_target(None)


def test_get_target_lambda():
    element.Frame.del_stack()
    el = ui.element()
    assert "#this" == el.get_target(lambda: "this")


def test_get_target_str():
    element.Frame.del_stack()
    el = ui.element()
    assert "#outerHTML" == el.get_target("outerHTML")
    assert "#asd" == el.get_target("asd")
    assert "this" == el.get_target("this")
    assert "#shouldbeok" == el.get_target("#shouldbeok")


def test_get_target_element_id():
    element.Frame.del_stack()
    el = ui.element()
    el2 = ui.element()
    assert f"#{el2.id}" == el.get_target(el2)


def test_oob_top_level():
    element.Frame.del_stack()
    with ui.element() as root:
        ui.toast("uiwiz")
    assert (
        '<div id="a-0"></div><div id="toast" hx-swap-oob="afterbegin"><div id="a-2" class="alert w-full z-50 "><span id="a-3">uiwiz</span></div></div>'
        == str(root)
    )
