from asyncio.events import AbstractEventLoop
from typing import Union
from wmp.asyncio import Transport


class FakeTransport():
    def __init__(self, asyncio: Transport, loop: AbstractEventLoop):
        self._asyncio = asyncio
        self._loop = loop
        self._last_data: str
        self._next_response: Union[str, None] = None
        self._ready = False

    async def wait_for_response(self):
        while True:
            if self._ready:
                if self._next_response:
                    self._asyncio.data_received(
                        bytes(self._next_response, "UTF-8"))
                self._ready = False
                return

    def write(self, data: bytes) -> None:
        self._last_data = data.decode("utf-8")
        self._ready = True

    def set_next_response(self, response: str):
        self._next_response = response

    def get_last_data(self):
        return self._last_data
