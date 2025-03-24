

# UiWizard

UiWizard is a python-based ui-framework for the web. It was inspired by the great framework [NiceGui](https://github.com/zauberzeug/nicegui). Why create this project that is very similar to NiceGui?
- The first reason was that NiceGui requires websockets to work and when experimenting with the framework it caused some issues on my hosting platform.
- Learning. I wanted to figure out how to do something simillar but without using websockets
  - I wanted to try out HTMX
- Limited control over the underlaying tech stack but mainly just learning

Example and docs
[UI-Wizard](https://ui-wizard.com/)

## Features

- Tailwind and DaisyUI for the graphics and responsive layout
- Webbased
- Quite a lot of standard elements, input fields, dropdown, foot, header, tabs...
- HTMX for interactivity
- Hopefully great defaults!

## Usage

Install the library

```
pip install uiwiz
```

Create a main.py file

```python
import uvicorn

from uiwiz import ui, UiwizApp

app = UiwizApp()


@app.page("/")
async def home_page():
    ui.label("Hello world")


if __name__ == "__main__":
    uvicorn.run(app)
```

Run it

```bash
python main.py
```

## General info

HTMX works with input fields in HTML and forms. To make it a bit easier to work with the form submit event does not send the data in the normal form format but uses the HTMX extension to convert it to json. This means that endpoints using UiWizard can use pydantic models as the input and have the benefit of validation.


## Tests

```bash
poetry run coverage run -m pytest .
```

```bash
poetry run coverage html
```
