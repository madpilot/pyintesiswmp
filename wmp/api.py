from typing import Awaitable, List, Union
from wmp.handler import CfgResult, CnfResult, IdResult, InfoResult, LimitsResult, PingResult
from wmp.asyncio import Transport


class API:
    def __init__(self, protocol: Transport):
        self._protocol = protocol

    def ping(self) -> Awaitable[PingResult]:
        return self._protocol.send("PING")

    def id(self) -> Awaitable[IdResult]:
        return self._protocol.send("ID")

    def info(self) -> Awaitable[List[InfoResult]]:
        return self._protocol.send("INFO")

    def set(self, ac_num: int, function: str, value: str) -> Awaitable[bool]:
        return self._protocol.send("SET,%i:%s,%s" % (ac_num, function, value))

    def get(self, ac_num: int, function: str) -> Awaitable[Union[CnfResult, List[CnfResult]]]:
        return self._protocol.send("GET,%i:%s" % (ac_num, function))

    def login(self, password: str):
        return self._protocol.send("LOGIN:%s" % (password))

    def logout(self) -> Awaitable[bool]:
        return self._protocol.send("LOGOUT")

    def send_config(self, item: str, value: str) -> Awaitable[bool]:
        return self._protocol.send("CFG:%s,%s" % (item, value))

    def get_config(self, item: str) -> Awaitable[CfgResult]:
        return self._protocol.send("CFG:%s" % (item))

    def set_limits(self, function: str, range: List[Union[str, int]]) -> Awaitable[bool]:
        range_str = map(lambda s: str(s), range)
        return self._protocol.send("LIMITS:%s,[%s]" % (function, ",".join(range_str)))

    def get_limits(self, function: str) -> Awaitable[LimitsResult]:
        return self._protocol.send("LIMITS:%s" % (function))
