from typing import List


def ping() -> str:
    return "PING"


def id() -> str:
    return "ID"


def info() -> str:
    return "INFO"


def set(ac_num: int, function: str, value: str) -> str:
    return "SET,%i:%s,%s" % (ac_num, function, value)


def get(ac_num: int, function: str) -> str:
    return "GET,%i:%s" % (ac_num, function)


def login(password: str) -> str:
    return "LOGIN:%s" % (password)


def logout() -> str:
    return "LOGOUT"


def send_config(item: str, value: str) -> str:
    return "CFG:%s,%s" % (item, value)


def get_config(item: str) -> str:
    return "CFG:%s" % (item)


def set_limits(function: str, range: List[str]) -> str:
    return "LIMITS:%s,[%s]" % (function, ",".join(range))


def get_limits(function: str) -> str:
    return "LIMITS:%s" % (function)
