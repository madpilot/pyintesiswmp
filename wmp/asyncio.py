import asyncio
from wmp import Handler


class AsyncIO(asyncio.Protocol):
    def __init__(self, handler):
        self.handler = Handler(handler)
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exception):
        self.transport = None

    def data_received(self, data):
        lines = data.decode("utf-8").split("\r\n")
        for line in lines:
            self.handler.parse(line)

    def send(self, message):
        if self.transport is not None:
            self.transport.write(bytes(message + "\r\n", "UTF-8"))
