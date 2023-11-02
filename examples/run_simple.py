from fastapi import Request
from pydantic import BaseModel
from uiwis.app import page, app
from uiwis.element import Element
import uiwis.ui as ui
import uvicorn

app.setup()

def create_nav():
    with ui.nav():
        ui.button("this is from a method")


@page("/")
async def test(request: Request):
    create_nav()
    with ui.element().classes(""):
        ui.markdown("""```python
if True:
    print "hi"
```""")


    with ui.footer():
        ui.label("some footer text")
    


if __name__ == "__main__":
    uvicorn.run("run_simple:app", reload=True)