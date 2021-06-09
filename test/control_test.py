from test.mocls.transport import FakeTransport
from wmp.handler import CfgResult, CnfResult, IdResult, InfoResult, LimitsResult, PingResult
from wmp.control import Control
import pytest
import asyncio
from asyncio.events import AbstractEventLoop
import wmp
from wmp.asyncio import Transport


@ pytest.fixture
def loop():
    return asyncio.get_event_loop()


@ pytest.fixture
def real_transport(loop: AbstractEventLoop):
    asyncio = wmp.Transport(loop)
    return asyncio


@ pytest.fixture
def transport(real_transport: Transport, loop: AbstractEventLoop) -> FakeTransport:
    t = FakeTransport(real_transport, loop)
    asyncio.run_coroutine_threadsafe(t.wait_for_response(), loop=loop)
    real_transport.connection_made(t)
    return t


@ pytest.fixture
def api(real_transport):
    return wmp.API(real_transport)


@pytest.fixture
def control(api):
    return Control(api)


@ pytest.mark.asyncio
async def test_get(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response(
        "ID:FJ-RC-WMP-1,CC3F1D0247A7,192.168.0.1,ASCII,v1.3.3,-50,WMP_000000,N,3")
    result = await control.get_id()
    assert transport.get_last_data() == "ID\r\n"
    assert result.__class__ == IdResult
    assert result.model == "FJ-RC-WMP-1"
    assert result.mac == "CC3F1D0247A7"
    assert result.ip == "192.168.0.1"
    assert result.protocol == "ASCII"
    assert result.version == "v1.3.3"
    assert result.rssi == -50
    assert result.device_id == "WMP_000000"


@ pytest.mark.asyncio
async def test_get_state(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("CHN,1:ONOFF,ON\r\n" +
                                "CHN,1:MODE,AUTO\r\n" +
                                "CHN,1:FANSP,AUTO\r\n" +
                                "CHN,1:VANEUD,AUTO\r\n" +
                                "CHN,1:VANELR,AUTO\r\n" +
                                "CHN,1:SETPTEMP,210\r\n" +
                                "CHN,1:AMBTEMP,-32768\r\n" +
                                "CHN,1:ERRSTATUS,OK\r\n" +
                                "CHN,1:ERRCODE,0")
    result = await control.get_state(1)
    assert transport.get_last_data() == "GET,1:*\r\n"
    assert len(result) == 9
    assert result[0].__class__ == CnfResult
    assert result[0].unit_number == 1
    assert result[0].function == "ONOFF"
    assert result[0].value == "ON"
    assert result[1].__class__ == CnfResult
    assert result[1].unit_number == 1
    assert result[1].function == "MODE"
    assert result[1].value == "AUTO"


@ pytest.mark.asyncio
async def test_set_power_on(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("ACK")
    result = await control.set_power(1, "ON")
    assert transport.get_last_data() == "SET,1:ONOFF,ON\r\n"
    assert result == True


@pytest.mark.asyncio
async def test_get_power_on(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("CHN,1:ONOFF,ON")
    result = await control.get_power(1)
    assert transport.get_last_data() == "GET,1:ONOFF\r\n"
    assert result == "ON"


@ pytest.mark.asyncio
async def test_get_power_off(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("CHN,1:ONOFF,OFF")
    result = await control.get_power(1)
    assert transport.get_last_data() == "GET,1:ONOFF\r\n"
    assert result == "OFF"


@ pytest.mark.asyncio
async def test_set_mode(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("ACK")
    result = await control.set_mode(1, "AUTO")
    assert transport.get_last_data() == "SET,1:MODE,AUTO\r\n"
    assert result == True


@ pytest.mark.asyncio
async def test_get_mode(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("CHN,1:MODE,AUTO")
    result = await control.get_mode(1)
    assert transport.get_last_data() == "GET,1:MODE\r\n"
    assert result == "AUTO"


@ pytest.mark.asyncio
async def test_set_set_point(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("ACK")
    result = await control.set_set_point(1, 23)
    assert transport.get_last_data() == "SET,1:SETPTEMP,23\r\n"
    assert result == True


@ pytest.mark.asyncio
async def test_get_mode(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("CHN,1:SETPTEMP,21.5")
    result = await control.get_set_point(1)
    assert transport.get_last_data() == "GET,1:SETPTEMP\r\n"
    assert result == 21.5


@ pytest.mark.asyncio
async def test_set_fan_speed(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("ACK")
    result = await control.set_fan_speed(1, "1")
    assert transport.get_last_data() == "SET,1:FANSP,1\r\n"
    assert result == True


@ pytest.mark.asyncio
async def test_get_mode(transport: FakeTransport, control: wmp.Control):
    transport.set_next_response("CHN,1:FANSP,2")
    result = await control.get_fan_speed(1)
    assert transport.get_last_data() == "GET,1:FANSP\r\n"
    assert result == "2"
