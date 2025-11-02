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
    ui.element(content="Memasdsade")
    ui.element(content="Memasdsade")

    logger.info("Calling index")
    
    return {}