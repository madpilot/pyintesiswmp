from wmp.commands import get_config, get_limits, login, logout, ping, id, info, send_config, set, get, set_limits


def test_ping():
    result = ping()
    assert result == "PING"


def test_id():
    result = id()
    assert result == "ID"


def test_info():
    result = info()
    assert result == "INFO"


def test_set():
    result = set(2, "ONOFF", "ON")
    assert result == "SET,2:ONOFF,ON"


def test_get():
    result = get(2, "ONOFF")
    assert result == "GET,2:ONOFF"


def test_login():
    result = login("password")
    assert result == "LOGIN:password"


def test_logout():
    result = logout()
    assert result == "LOGOUT"


def test_send_config():
    result = send_config("PIN", "12345678")
    assert result == "CFG:PIN,12345678"


def test_get_config():
    result = get_config("PIN")
    assert result == "CFG:PIN"


def test_set_limits():
    result = set_limits("SETPTEMP", ["180", "280"])
    assert result == "LIMITS:SETPTEMP,[180,280]"


def test_get_limits():
    result = get_limits("SETPEMP")
    assert result == "LIMITS:SETPEMP"
