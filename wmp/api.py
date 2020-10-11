class API:
    def __init__(self, transport):
        self._transport = transport

    def ping(self):
        self._transport.send("PING")

    def id(self):
        self._transport.send("ID")

    def info(self):
        self._transport.send("INFO")

    def set(self, ac_num, function, value):
        self._transport.send("SET,%i:%s,%s" % (ac_num, function, value))

    def get(self, ac_num, function):
        self._transport.send("GET,%i:%s" % ac_num, function)

    def login(self, password):
        self._transport.send("LOGIN:%s" % password)

    def logout(self):
        self._transport.send("LOGOUT")

    def send_config(self, item, value):
        self._transport.send("CFG:%s,%s" % item, value)

    def get_config(self, item):
        self._transport.send("CFG:%" % item)

    def set_limits(self, function, range):
        self._transport.send("LIMITS:%s,%s" % function, range)

    def get_limits(self, function):
        self._transport.send("LIMITS:%s" % function)
