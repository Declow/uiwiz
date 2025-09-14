import uvicorn

from src import ui
from src.app import UiwizApp

app = UiwizApp()


@app.page("/")
async def home_page():
    ui.label("Hello world")


if __name__ == "__main__":
    uvicorn.run(app)
