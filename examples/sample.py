from uiwiz import ui, UiwizApp, server

app = UiwizApp()


@app.page("/")
async def home_page():
    ui.label("Hello world")


if __name__ == "__main__":
    server.run(app)
