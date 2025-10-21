import asyncio
from asyncio import Queue, Event
from typing import Any
from pydantic import BaseModel

from uiwiz.app import UiwizApp
import logging

logger = logging.getLogger(__name__)

class Config(BaseModel):
    host: str
    port: int
    app: UiwizApp


class LifespanHandler:

    def __init__(self, config: Config):
        self.config = config
        self.receive_queue: Queue = Queue()
        self.state: dict[str, Any] = {}
        self.startup_done_event = Event()
        self.shutdown_done_event = Event()
        
    async def startup(self) -> None:
        logger.info("Calling lifespan")
        loop = asyncio.get_event_loop()
        lifespan_task = loop.create_task(self.execute())
        await self.receive_queue.put({"type": "lifespan.startup"})
        await self.startup_done_event.wait()

        logger.info("Startup complete")
    
    async def execute(self) -> None:
        app = self.config.app
        scope = {
            "type": "lifespan",
            "asgi": {"version": "3", "spec_version": "2.0"},
            "state": self.state,
        }
        await app(scope, self.receive_queue, self.send)

    async def send(self, message: dict) -> None:
        task = {
            "lifespan.startup.complete": lambda: self.startup_done_event.set(),
            "lifespan.startup.failed": lambda: self.startup_done_event.set(),
            "lifespan.shutdown.complete": lambda: self.shutdown_done_event.set(),
            "lifespan.shutdown.failed": lambda: self.shutdown_done_event.set()
        }
        task.get(message["type"], lambda: 1)()


def create_socket():
    pass



class Server:
    def __init__(self):
        pass

