from uiwiz import ui, UiwizApp
import logging
from contextlib import asynccontextmanager
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app):
    logger.info("Start app")
    yield
    logger.info("Closing app")


app = UiwizApp(lifespan=lifespan)


@app.page("/")
def index():
    ui.element(content="This is pretty cool")
    ui.element(content="Custom server working!")

    logger.info("Calling index")
    
    return {}