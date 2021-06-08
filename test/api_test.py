from wmp.handler import CfgResult, CnfResult, IdResult, InfoResult, LimitsResult, PingResult
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
async def test_ping(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("PONG:-51")
    result = await api.ping()
    assert result.__class__ == PingResult
    assert result.rssi == -51
    assert transport.get_last_data() == "PING\r\n"


@ pytest.mark.asyncio
async def test_id(transport: FakeTransport, api: wmp.API):
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
    assert transport.get_last_data() == "ID\r\n"


@ pytest.mark.asyncio
async def test_info(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("INFO:APPVERSION,1.0.0.1\r\n" +
                                "INFO:RUNVERSION,1.3.3\r\n" +
                                "INFO:CFGVERSION,1.2.3\r\n" +
                                "INFO:WLANVERSION,2.0.0\r\n" +
                                "INFO:DEVICEINFO,FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\r\n" +
                                "INFO:HASH,0D00:0101")
    result = await api.info()
    assert len(result) == 6
    assert result[0].__class__ == InfoResult
    assert result[0].info_type == "APPVERSION"
    assert result[0].value == "1.0.0.1"
    assert result[1].__class__ == InfoResult
    assert result[1].info_type == "RUNVERSION"
    assert result[1].value == "1.3.3"
    assert result[2].__class__ == InfoResult
    assert result[2].info_type == "CFGVERSION"
    assert result[2].value == "1.2.3"
    assert result[3].__class__ == InfoResult
    assert result[3].info_type == "WLANVERSION"
    assert result[3].value == "2.0.0"
    assert result[4].__class__ == InfoResult
    assert result[4].info_type == "DEVICEINFO"
    assert result[4].value == "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    assert result[5].__class__ == InfoResult
    assert result[5].info_type == "HASH"
    assert result[5].value == "0D00:0101"
    assert transport.get_last_data() == "INFO\r\n"


@ pytest.mark.asyncio
async def test_set(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("ACK")
    result = await api.set(1, "ONOFF", "ON")
    assert result == True
    assert transport.get_last_data() == "SET,1:ONOFF,ON\r\n"


@ pytest.mark.asyncio
async def test_get(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("CHN,1:MODE,AUTO")
    result = await api.get(1, "MODE")
    assert result.__class__ == CnfResult
    assert result.unit_number == 1
    assert result.function == "MODE"
    assert result.value == "AUTO"
    assert transport.get_last_data() == "GET,1:MODE\r\n"


@ pytest.mark.asyncio
async def test_logout(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("OK")
    result = await api.logout()
    assert result == True
    assert transport.get_last_data() == "LOGOUT\r\n"


@ pytest.mark.asyncio
async def test_send_config(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("ACK")
    result = await api.send_config("PIN", "12345678")
    assert result == True
    assert transport.get_last_data() == "CFG:PIN,12345678\r\n"


@ pytest.mark.asyncio
async def test_get_config(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("CFG:DATETIME,28/08/2000 02:38:08")
    result = await api.get_config("DATETIME")
    assert result.__class__ == CfgResult
    assert result.config == "DATETIME"
    assert result.value == "28/08/2000 02:38:08"
    assert transport.get_last_data() == "CFG:DATETIME\r\n"


@ pytest.mark.asyncio
async def test_set_limits(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("ACK")
    result = await api.set_limits("SETPTEMP", [180, 280])
    assert result == True
    assert transport.get_last_data() == "LIMITS:SETPTEMP,[180,280]\r\n"


@ pytest.mark.asyncio
async def test_get_limits(transport: FakeTransport, api: wmp.API):
    transport.set_next_response("LIMITS:ONOFF,[OFF,ON]")
    result = await api.get_limits("ONOFF")
    assert result.__class__ == LimitsResult
    assert result.function == "ONOFF"
    assert result.limits == ["OFF", "ON"]
    assert transport.get_last_data() == "LIMITS:ONOFF\r\n"
