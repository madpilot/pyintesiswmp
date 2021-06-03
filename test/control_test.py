from wmp.handler import IdResult, PingResult
import pytest
import asyncio
from asyncio.events import AbstractEventLoop
from typing import Union
import wmp
from wmp.asyncio import Asyncio


class FakeTransport():
    def __init__(self, asyncio: Asyncio, loop: AbstractEventLoop):
        self._asyncio = asyncio
        self._loop = loop
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
        self._ready = True

    def set_next_response(self, response: str):
        self._next_response = response


@ pytest.fixture
def loop():
    return asyncio.get_event_loop()


@ pytest.fixture
def wmp_asyncio(loop: AbstractEventLoop):
    asyncio = wmp.Asyncio(loop)
    return asyncio


@ pytest.fixture
def transport(wmp_asyncio: Asyncio, loop: AbstractEventLoop) -> FakeTransport:
    t = FakeTransport(wmp_asyncio, loop)
    asyncio.run_coroutine_threadsafe(t.wait_for_response(), loop=loop)
    wmp_asyncio.connection_made(t)
    return t


@ pytest.fixture
def api(wmp_asyncio):
    return wmp.API(wmp_asyncio)


@ pytest.mark.asyncio
async def test_ping(transport: FakeTransport, api: wmp.API, loop: AbstractEventLoop):
    transport.set_next_response("PONG:-51")
    result = await api.ping()
    assert result.__class__ == PingResult
    assert result.rssi == -51


@ pytest.mark.asyncio
async def test_id(transport: FakeTransport, api: wmp.API, loop: AbstractEventLoop):
    transport.set_next_response(
        "ID:FJ-RC-WMP-1,CC3F1D0247A7,192.168.0.1,ASCII,v1.3.3,-50,WMP_000000,N,3")
    result = await api.id()
    assert result.__class__ == IdResult
    assert result.model == "FJ-RC-WMP-1"
    assert result.mac == "CC3F1D0247A7"
    assert result.ip == "192.168.0.1"
    assert result.protocol == "ASCII"
    assert result.version == "v1.3.3"
    assert result.rssi == -50
    assert result.device_id == "WMP_000000"
