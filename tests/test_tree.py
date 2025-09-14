from bs4 import BeautifulSoup

from src import ui
from src.frame import Frame


def test_correct_parent():
    with ui.element() as root_1:
        with ui.element() as child_1_1:
            ui.element(content="test_1")

    with ui.element():
        with ui.element() as child_2_1:
            with child_1_1:
                ui.element(content="test_2")
            ui.element(content="test_3")

    soup = BeautifulSoup(Frame.get_stack().render(), "html.parser")

    assert len(child_2_1.children) == 1
    assert len(root_1.children) == 1
    assert (
        soup.prettify()
        == """<div id="a-0">
 <div id="a-1">
  <div id="a-2">
   test_1
  </div>
  <div id="a-5">
   test_2
  </div>
 </div>
</div>
<div id="a-3">
 <div id="a-4">
  <div id="a-6">
   test_3
  </div>
 </div>
</div>
"""
    )


def test_correct_parent_deep():
    with ui.element() as root_1:
        with ui.element() as child_1_1:
            ui.element(content="test_1")

    with ui.element():
        with ui.element() as child_2_1:
            with child_1_1:
                with ui.element(content="test_2"):
                    with ui.element() as child_2_2:
                        ui.element(content="test_4")
            ui.element(content="test_3")

    soup = BeautifulSoup(Frame.get_stack().render(), "html.parser")

    assert len(child_2_1.children) == 1
    assert len(root_1.children) == 1
    assert (
        soup.prettify()
        == """<div id="a-0">
 <div id="a-1">
  <div id="a-2">
   test_1
  </div>
  <div id="a-5">
   test_2
   <div id="a-6">
    <div id="a-7">
     test_4
    </div>
   </div>
  </div>
 </div>
</div>
<div id="a-3">
 <div id="a-4">
  <div id="a-8">
   test_3
  </div>
 </div>
</div>
"""
    )
