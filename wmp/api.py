from typing import List
from wmp.asyncio import Asyncio


class API:
    def __init__(self, protocol: Asyncio):
        self._protocol = protocol

    def ping(self):
        return self._protocol.send("PING")

    def id(self):
        return self._protocol.send("ID")

    def info(self):
        return self._protocol.send("INFO")

    def set(self, ac_num: int, function: str, value: str):
        return self._protocol.send("SET,%i:%s,%s" % (ac_num, function, value))

    def get(self, ac_num: int, function: str):
        return self._protocol.send("GET,%i:%s" % (ac_num, function))

    def login(self, password: str):
        return self._protocol.send("LOGIN:%s" % (password))

    def logout(self):
        return self._protocol.send("LOGOUT")

    def send_config(self, item: str, value: str):
        return self._protocol.send("CFG:%s,%s" % (item, value))

    def get_config(self, item: str):
        return self._protocol.send("CFG:%s" % (item))

    def set_limits(self, function: str, range: List[str]):
        range_str = map(lambda s: str(s), range)
        return self._protocol.send("LIMITS:%s,[%s]" % (function, ",".join(range_str)))

    def get_limits(self, function: str):
        return self._protocol.send("LIMITS:%s" % (function))
