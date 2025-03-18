from pydantic import BaseModel

from uiwiz import ui
from uiwiz.app import UiwizApp
from uiwiz.frame import Frame


class DataInput(BaseModel):
    name: str
    age: int


def test_model_handler():
    ui.modelForm(DataInput)
    output = Frame.get_stack().render()
    expected = """<form id="a-0" class="flex flex-col items-start gap-4 p-4  border border-base-content rounded-lg shadow-lg w-full"><div id="a-1" class="flex flex-nowrap w-full"><input id="a-3" class="input  input-bordered w-full input-md" name="name" placeholder="name" autocomplete="off"></div><div id="a-4" class="flex flex-nowrap w-full"><input id="a-6" class="input  input-bordered w-full input-md" name="age" placeholder="age" autocomplete="off"></div></form>"""
    assert expected == output

def test_model_handler_instance():
    ui.modelForm(DataInput(name="John", age=30))
    output = Frame.get_stack().render()
    expected = """<form id="a-0" class="flex flex-col items-start gap-4 p-4  border border-base-content rounded-lg shadow-lg w-full"><div id="a-1" class="flex flex-nowrap w-full"><input id="a-3" class="input  input-bordered w-full input-md" name="name" placeholder="name" value="John" autocomplete="off"></div><div id="a-4" class="flex flex-nowrap w-full"><input id="a-6" class="input  input-bordered w-full input-md" name="age" placeholder="age" value="30" autocomplete="off"></div></form>"""
    assert expected == output

def test_model_handler_instance_submit():
    app = UiwizApp()

    @app.ui("/submit")
    async def submit():
        pass

    ui.modelForm(DataInput(name="John", age=30)).on_submit(submit)
    output = Frame.get_stack().render()
    expected = """<form id="a-0" class="flex flex-col items-start gap-4 p-4  border border-base-content rounded-lg shadow-lg w-full" hx-target="this" hx-swap="none" hx-post="/submit" hx-trigger="submit" hx-ext="json-enc"><div id="a-1" class="flex flex-nowrap w-full"><input id="a-3" class="input  input-bordered w-full input-md" name="name" placeholder="name" value="John" autocomplete="off"></div><div id="a-4" class="flex flex-nowrap w-full"><input id="a-6" class="input  input-bordered w-full input-md" name="age" placeholder="age" value="30" autocomplete="off"></div><button id="a-7" class="btn btn-md">Save</button></form>"""
    assert expected == output