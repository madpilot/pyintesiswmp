from typing import List


class API:
    def __init__(self, transport):
        self._transport = transport

    def ping(self):
        return self._transport.send("PING")

    def id(self):
        return self._transport.send("ID")

    def info(self):
        return self._transport.send("INFO")

    def set(self, ac_num: int, function: str, value: str):
        return self._transport.send("SET,%i:%s,%s" % (ac_num, function, value))

    def get(self, ac_num: int, function: str):
        return self._transport.send("GET,%i:%s" % (ac_num, function))

    def login(self, password: str):
        return self._transport.send("LOGIN:%s" % (password))

    def logout(self):
        return self._transport.send("LOGOUT")

    def send_config(self, item: str, value: str):
        return self._transport.send("CFG:%s,%s" % (item, value))

    def get_config(self, item: str):
        return self._transport.send("CFG:%s" % (item))

    def set_limits(self, function: str, range: List[str]):
        return self._transport.send("LIMITS:%s,%s" % (function, ",".join(range)))

    def get_limits(self, function: str):
        return self._transport.send("LIMITS:%s" % (function))
