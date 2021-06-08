import re
from typing import List, Union


class IdResult:
    def __init__(self, model: str, mac: str, ip: str, protocol: str, version: str, rssi: str, device_id: str, _y: str, _x: str):
        self.model: str = model
        self.mac: str = mac
        self.ip: str = ip
        self.protocol: str = protocol
        self.version: str = version
        self.rssi: int = int(rssi)
        self.device_id: str = device_id
        self._y: str = _y
        self._x: str = _x


class InfoResult:
    def __init__(self, info_type: str, value: str):
        self.info_type: str = info_type
        self.value: str = value


class LimitsResult:
    def __init__(self, function: str, limits: List[str]):
        self.function = function
        self.limits = limits


class CnfResult:
    def __init__(self, unit_number: int, function: str, value: str):
        self.unit_number: int = unit_number
        self.function: str = function
        self.value: str = value


class PingResult:
    def __init__(self, rssi: int):
        self.rssi = rssi


class CfgResult:
    def __init__(self, config: str, value: str):
        self.config = config
        self.value = value


def parse(message: str) -> Union[PingResult, IdResult, InfoResult, LimitsResult, CnfResult, CfgResult, bool, None]:
    name = ""
    arguments = ""
    parts = message.split(":")

    if len(parts) == 1:
        [name] = parts
    if len(parts) >= 2:
        name = parts.pop(0)
        arguments = ":".join(parts)

    if name == "PONG":
        return PingResult(int(arguments))

    if name == "ID":
        [model, mac, ip, protocol, version, rssi,
            device_id, _y, _x] = arguments.split(",")
        return IdResult(model, mac, ip, protocol, version, rssi,  device_id, _y, _x)

    if name == "INFO":
        [type, value] = arguments.split(",")
        return InfoResult(type, value)

    if name == "ACK":
        return True

    if name == "OK":
        return True

    if name == "CFG":
        [config, value] = arguments.split(",")
        return CfgResult(config, value)

    results = re.match(r'LIMITS:(.+),\[(.+)\]', message)
    if results is not None:
        function = results.group(1)
        limits = results.group(2).split(',')
        return LimitsResult(function, limits)

    results = re.match(r'CHN,(\d+):(.+)', message)
    if results is not None:
        unit_number = int(results.group(1))
        [function, value] = results.group(2).split(",")
        return CnfResult(unit_number, function, value)

    return None
