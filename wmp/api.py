class API:
    def __init__(self, transport):
        self._transport = transport

    def ping(self):
        return self._transport.send("PING")

    def id(self):
        return self._transport.send("ID")

    def info(self):
        return self._transport.send("INFO")

    def set(self, ac_num, function, value):
        return self._transport.send("SET,%i:%s,%s" % (ac_num, function, value))

    def get(self, ac_num, function):
        return self._transport.send("GET,%i:%s" % (ac_num, function))

    def login(self, password):
        return self._transport.send("LOGIN:%s" % (password))

    def logout(self):
        return self._transport.send("LOGOUT")

    def send_config(self, item, value):
        return self._transport.send("CFG:%s,%s" % (item, value))

    def get_config(self, item):
        return self._transport.send("CFG:%s" % (item))

    def set_limits(self, function, range):
        return self._transport.send("LIMITS:%s,%s" % (function, range))

    def get_limits(self, function):
        return self._transport.send("LIMITS:%s" % (function))
