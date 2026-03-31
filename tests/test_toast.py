from uiwiz import ui


def test_toast_default_render_contains_toast_data() -> None:
    output = str(ui.toast("Saved"))
    assert 'id="toast"' in output
    assert "hx-toast-data" in output
    assert "Saved" in output


def test_toast_error_disables_auto_close_and_has_close_button() -> None:
    output = str(ui.toast("Oops").error())
    assert "autoClose" in output
    assert "false" in output
    assert "btn-circle" in output
