from src import ui


def test_frame_id_reuse():
    # setup
    from src.frame import get_request

    get_request().headers = {"hx-target": "a-1", "hx-swap": "outerHTML"}

    # Init
    first_ele = ui.element()
    ele = ui.element()

    assert "a-1" == first_ele.id
    assert "a-1" != ele.id
