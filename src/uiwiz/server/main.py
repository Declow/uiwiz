from uiwiz import ui, UiwizApp

app = UiwizApp()

@app.page("/")
def index():
    ui.element(content="Meme")
    return {}