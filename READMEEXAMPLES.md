
# Setup

These examples expect that the user has setup the initial application like
the following code snippet.
The examples should be inserted into the home_page function.

It is recommended to use a virtual environment like poetry or pipenv.

Create a main.py file

```python
from uiwiz.app import UiwizApp
import uiwiz.ui as ui
import uvicorn

app = UiwizApp()

@app.page("/")
async def home_page(request: Request):
    ui.label("Hello world")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
```

Run it

```bash
python main.py
```


# Components

UiWizard has a lot of different components ready to be used.
This Markdown will show some examples of how to use them.

Label

```python
ui.label("Hello world")
```

Button

```python
ui.button("Click me")
```

A button is pretty useless if there is no action associated with it

```python
@app.ui("/swap-button")
def swap_button():
    ui.label("Button swapped")

ui.button("Click me").on_click(endpoint="/swap-button")
```

What if I want to change another element with the button?

```python
@app.ui("/swap-label")
def swap_button():
    ui.label("After click")

_target = ui.label("Before click")
ui.button("Click me").on_click(endpoint="/swap-label", target=_target.id)
```

But what if a want to have the button defined before the label?
```python
@app.ui("/swap-label")
def swap_button():
    ui.label("After click")

ui.button("Click me").on_click(endpoint="/swap-label", target=lambda: _target.id)
_target = ui.label("Before click")
```

## Inputs

Checkbox
```python
ui.checkbox("box_to_check", checked=True)
# checkbox with text
with ui.row():
    c = ui.checkbox("box_to_check")
    ui.label("UiWizard user", for_=c)
```

Builtin browser datepicker
```python
from datetime import datetime
ui.datepicker("UiWizard_user", datetime.now())
```

Dropdown menu
```python
ui.dropdown(["item 1", "item 2"], "Pick item")
```

Bind an input field to a label
```python
ui.input("input name", "first_name")

# Bind text to input
last_name = ui.input("input last name", name="last_name")
ui.label().bind_text_from(last_name)
```

Radio input
```python
# radio with text next to it
with ui.row():
    r = ui.radio("test_radio", "htmx")
    ui.label("htmx", r)
with ui.row():
    r1 = ui.radio("test_radio", "javascript")
    ui.label("javascript", r1)
```

Range input with label
```python
range = ui.range(0, 100, 0, "value")
ui.label(range.value).bind_text_from(range)
```

Textarea
```python
ui.textarea(name="description")
```

A toggle
```python
ui.toggle("active_feature")
```

Upload file
```python
# TODO: Update upload to handle endpoint instead of function
ui.upload(name="file", on_upload=handle_upload, target=lambda: table.id)
```

## Toast

It is possible to inform the client with a message when a request is done to
inform the user of the result of their action.
```python
@app.ui("/form/handle_input")
async def handle_input(data: FormInput):
    failed = action()
    if failed:
        with ui.toast().error():
            ui.label("Failed to save item")
    else:
        with ui.toast().success():
            ui.label("Item Saved")
```

The error or success function adds an svg indication
possible methods
- success
- error
- warning
- info
- menu

```python

@app.ui()
def action_on_server():
    with ui.element():
        ui.label("")
# TODO: Update upload to handle endpoint instead of function
ui.upload(name="file", on_upload=handle_upload, target=lambda: table.id)
```

## Data elements

TODO


## Form

When working with UiWizard the input will often be in a html form.
As UiWizard uses fastapi it is possible to use pydantic models for
handling validation of data input.

```python
# Define an input model
from pydantic import BaseModel

# Create the input model sent from the server
class FormInput(BaseModel):
    first_name: str

# Create the endpoint the form submit must use
@app.ui("/form/handle_input")
def handle_input(data_input: FormInput):
    with ui.toast():
        ui.label("Saved data") # Creates a toast message

@app.page("/")
async def home_page(request: Request):
    # Create the form and specify the endpoint
    with ui.form().on_submit(endpoint="/form/handle_input"):
        ui.input(name="first_name") # name must match FromInput names
        ui.button("Submit")

```

Currently missing a good way to display to the user, which form input is missing or
the validation failed.

## Usage

Create a main.py file

```python
from uiwiz.app import UiwizApp
import uiwiz.ui as ui
import uvicorn

app = UiwizApp()

@app.page("/")
async def home_page(request: Request):
    ui.label("Hello world")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
```

Run it

```bash
python main.py
```

# Styling

UiWizard has a lot of ways to handle styling.

```python
# Every element has a classes method
# See tailwind or daisyui for possible values
ui.element().classes("bg-base-100") # sets the color of the element
```
```python
# Want to have an inline style?
# A method will be created for convenience but this way will not be removed
ui.element().attributes["style"] = "margin-left: 2em;"
```

```python
# Navigation bar
with ui.nav():
    with ui.element("li"):
        ui.link("Second page", "/page-2")
```

```python
with ui.row():
    # elements created under row will be on the same line
    ui.label("test")
    ui.label("test")
```

```python
with ui.col():
    # elements created under row will be on the same line
    ui.label("test")
    ui.label("test")
```

```python
ui.divider()
```

```python
with ui.footer():
    # Creates a foot on the page
```

Drawer example.
This shows how to create a drawer on the left that auto hides when the screen
gets too small and shows a hamburger menu when the screen is too small.
```python
from uiwiz.svg.svg_handler import get_svg

with ui.drawer(always_open=True, right=False) as drawer:
    with drawer.drawer_content():
        with ui.element().classes(
            "sticky top-0 flex h-16 justify-center bg-opacity-90 backdrop-blur transition-shadow duration-100 [transform:translate3d(0,0,0)] shadow-sm"
        ):
            with ui.nav().classes("w-full navbar"):
                with ui.label(for_=drawer.drawer_toggle).classes("btn drawer-button lg:hidden"):
                    ui.html(get_svg("menu"))

        ui.label("test1")
        with ui.footer():
            ui.label("some footer text")

    with drawer.drawer_side():
        with ui.element("li"):
            ui.link("drawer-2", "/drawer-2")
            ui.link("Some link", "https://google.com")
```

# Custom components

It is possible to implement custom components, which is implemented in JS.
I would suggest look at the source code of aggrid. It uses the Ag grid library
to make a more feature rich table then what is possible with good old HTML.

It consists of 3 parts. The JS library itself as a script file. A python element
class, which makes the initial setup in the dom and a bit of glue JS in the aggrid.js
file, which handles the initial setup of the grid and the updates to the grid afterwards.

