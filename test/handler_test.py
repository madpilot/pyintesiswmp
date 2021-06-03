from wmp.handler import IdResult, parse


def test_id():
    result = parse(
        "ID:FJ-RC-WMP-1,CC3F1D0247A7,192.168.0.1,ASCII,v1.3.3,-50,WMP_000000,N,3")
    assert result.model == "FJ-RC-WMP-1"
    assert result.mac == "CC3F1D0247A7"
    assert result.ip == "192.168.0.1"
    assert result.protocol == "ASCII"
    assert result.version == "v1.3.3"
    assert result.rssi == -50
    assert result.device_id == "WMP_000000"


def test_info():
    result = parse("INFO:APPVERSION,1.0.0.1")
    assert result.info_type == "APPVERSION"
    assert result.value == "1.0.0.1"


def test_ack():
    result = parse("ACK")
    assert result == True


def test_ok():
    result = parse("OK")
    assert result == True


def test_cfg():
    result = parse("CFG")
    assert result == True


def test_limits():
    result = parse("LIMITS:ONOFF,[OFF,ON]")
    assert result.function == "ONOFF"
    assert result.limits == ["OFF", "ON"]


def test_chn():
    result = parse("CHN,1:ONOFF,ON")
    assert result.unit_number == 1
    assert result.function == "ONOFF"
    assert result.value == "ON"
