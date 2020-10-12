import re


class IdResult:
    def __init__(self, model, mac, ip, protocol, version, rssi, device_id, _y, _x):
        self.model = model
        self.mac = mac
        self.ip = ip
        self.protocol = protocol
        self.version = version
        self.rssi = rssi
        self.device_id = device_id
        self._y = _y
        self._x = _x


class CnfResult:
    def __init__(self, function, value):
        self.function = function
        self.value = value


def parse(message):
    name = ""
    arguments = ""
    parts = message.split(":")
    if len(parts) >= 2:
        [name, arguments] = parts

    if name == "ID":
        [model, mac, ip, protocol, version, rssi,
            device_id, _y, _x] = arguments.split(",")
        return IdResult(model, mac, ip, protocol, version, rssi,  device_id, _y, _x)

    if name == "INFO":
        return True

    if name == "ACK":
        return True

    if name == "OK":
        return True

    if name == "CFG":
        return True

    if name == "LIMITS":
        return True

    results = re.match(r'CHN,(\d+):(.+)', message)
    if results is not None:
        [function, value] = results.group(2).split(",")
        return CnfResult(function, value)

    return None
