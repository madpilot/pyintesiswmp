import asyncio
import re
from wmp import Handler


class Asyncio(asyncio.Protocol):
    def __init__(self, handler, loop):
        self.handler = Handler(handler)
        self.transport = None
        self.loop = loop
        self.next = None

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exception):
        self.transport = None

    def data_received(self, data):
        lines = data.decode("utf-8").split("\r\n")

        # If the command looks like a configuration change, let the callback handler
        # deal with that, other wise ship it off to the
        results = re.match(r'CHN,(\d+):(.+)', lines[0])
        if results is not None:
            [function, value] = results.group(2).split(",")
            self.handler.parse_change(results.group(1), function, value)
        else:
            if self.next is not None:
                self.next.set_result(
                    self.handler.parse(lines[0]))
                self.next = None

    def send(self, message):
        if self.transport is not None:
            self.transport.write(bytes(message + "\r\n", "UTF-8"))
            self.next = self.loop.create_future()
            return self.next
        else:
            future = self.loop.create_future()
            future.set_result(None)
            return future
