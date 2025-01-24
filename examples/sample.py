import uvicorn

from uiwiz import ui
from uiwiz.app import UiwizApp

app = UiwizApp()


@app.page("/")
async def home_page():
    ui.label("Hello world")


if __name__ == "__main__":
    uvicorn.run(app)
