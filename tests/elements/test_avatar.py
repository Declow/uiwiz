from unittest import mock

from uiwiz import ui
from uiwiz.app import UiwizApp
from uiwiz.frame import Frame
from uiwiz.page_route import PageRouter


def test_avatar():
    output = str(ui.avatar("/some/image/path"))
    assert (
        '<div id="a-0"><div id="a-1" class="w-12 rounded-full"><img id="a-2" src="/some/image/path"></div></div>'
        == output
    )


def test_avatar_classes():
    avatar = ui.avatar("/some/image/path")
    avatar.classes("w-18 rounded-full")
    output = str(avatar)
    assert (
        '<div id="a-0"><div id="a-1" class="w-18 rounded-full"><img id="a-2" src="/some/image/path"></div></div>'
        == output
    )
