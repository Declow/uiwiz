from pydantic import BaseModel

from uiwiz import ui
from uiwiz.frame import Frame


class DataInput(BaseModel):
    name: str
    age: int


def test_model_handler():
    ui.modelForm(DataInput)
    output = Frame.get_stack().render()
    expected = """<form id="a-0" class="flex flex-col items-start gap-4 p-4  border border-base-content rounded-lg shadow-lg w-full"><div id="a-1" class="flex flex-nowrap w-full"><input id="a-3" class="input  input-bordered w-full input-md" name="name" placeholder="name" autocomplete="off"></div><div id="a-4" class="flex flex-nowrap w-full"><input id="a-6" class="input  input-bordered w-full input-md" name="age" placeholder="age" autocomplete="off"></div></form>"""
    assert expected == output
