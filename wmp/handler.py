import re


class Handler:
    def __init__(self, callback):
        self.callback = callback

    def parse(self, message):
        [name, arguments] = message.split(":")

        if name == "ID":
            [model, mac, ip, protocol, version, rssi,
                _z, _y, _x] = arguments.split(",")
            self.callback.id(model, mac, ip, protocol, version, rssi)

        if name == "INFO":
            self.callback.info(arguments.split(","))

        if name == "ACK":
            self.callback.ack()

        if name == "OK":
            self.callback.ok()

        if name == "CFG":
            self.callback.cfg(arguments.split(","))

        if name == "LIMITS":
            self.callback.limits(arguments.split(","))

        results = re.match(r'CHN,(\d+)', name)
        if results:
            [function, value] = arguments.split(",")
            self.callback.change(results.group(1), function, value)
            self.parse_change(results.group(1), function, value)

    def parse_change(self, ac_num, function, value):
        if function == "ONOFF":
            self.callback.power(ac_num, value)

        if function == "MODE":
            self.callback.mode(ac_num, value)

        if function == "SETPTEMP":
            self.callback.set_point(ac_num, float(value) / 10)

        if function == "FANSP":
            self.callback.fan_speed(ac_num, value)
