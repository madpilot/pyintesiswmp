def ping():
    return "PING"


def id():
    return "ID"


def info():
    return "INFO"


def set(ac_num, function, value):
    return "SET,%i:%s,%s" % (ac_num, function, value)


def get(ac_num, function):
    return "GET,%i:%s" % (ac_num, function)


def login(password):
    return "LOGIN:%s" % (password)


def logout():
    return "LOGOUT"


def send_config(item, value):
    return "CFG:%s,%s" % (item, value)


def get_config(item):
    return "CFG:%s" % (item)


def set_limits(function, range):
    return "LIMITS:%s,%s" % (function, range)


def get_limits(function):
    return "LIMITS:%s" % (function)
