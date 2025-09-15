from uiwiz import ui


def test_upload_element():
    ele = ui.upload(name="file-upload")
    assert (
        '<input id="a-0" class="file-input file-input-bordered file-input-sm" type="file" name="file-upload">'
        == str(ele)
    )
