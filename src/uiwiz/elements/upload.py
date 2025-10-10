from uiwiz.elements.extensions.on_event import OnEvent
from uiwiz.event import FUNC_TYPE, ON_EVENTS, SWAP_EVENTS, TARGET_TYPE


class Upload(OnEvent):
    root_class: str = "file-input"
    root_size: str = "file-input-{size}"
    _classes: str = "file-input-bordered"

    def __init__(
        self,
        name: str,
    ) -> "Upload":
        """Upload

        This element is used for file uploads

        .. code-block:: python
            from uiwiz import ui
            from fastapi import UploadFile

            @app.ui("/upload/endpoint")
            async def handle_upload(file: UploadFile):
                file_output = await file.read()
                ui.toast(file_output.decode("utf-8")).success()

            ui.upload("file").on_upload(on_upload=handle_upload, swap="none")

        """
        super().__init__("input")
        self.attributes["type"] = "file"
        self.attributes["name"] = name
        self._size = "sm"
        self.classes(Upload._classes)

    def on_upload(
        self,
        on_upload: FUNC_TYPE,
        target: TARGET_TYPE = None,
        trigger: ON_EVENTS = "change",
        swap: SWAP_EVENTS = None,
    ) -> "Upload":
        """
        :param on_upload: The function to call when the upload event is triggered or the endpoint to call
        :param target: The target to swap the response to
        :param trigger: The event to trigger the function
        :param swap: The swap event to use
        """
        self.event = {
            "func": on_upload,
            "trigger": trigger,
            "target": target,
            "swap": swap,
            "hx-encoding": "multipart/form-data",
        }

        return self
