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


class Handler:
    def __init__(self, callback):
        self.callback = callback

    def parse(self, message):
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

    def parse_change(self, ac_num, function, value):
        if function == "ONOFF":
            self.callback.power(ac_num, value)

        if function == "MODE":
            self.callback.mode(ac_num, value)

        if function == "SETPTEMP":
            self.callback.set_point(ac_num, float(value) / 10)

        if function == "FANSP":
            self.callback.fan_speed(ac_num, value)
