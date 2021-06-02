import asyncio
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from types import FunctionType
from typing import Union
from wmp.handler import parse


class Asyncio(asyncio.Protocol):
    def __init__(self, loop: AbstractEventLoop, callback: FunctionType = None):
        self.transport = None
        self.loop = loop
        self.callback: Union[None, FunctionType] = callback
        self.next = None
        self.disconnection_callback = None

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exception):
        self.transport = None
        if self.disconnection_callback is not None:
            self.disconnection_callback()

    def data_received(self, data):
        lines = data.decode("utf-8").strip().split("\r\n")

        # If the command looks like a configuration change, let the callback handler
        # deal with that, other wise ship it off to the
        results = list(map(lambda line: parse(line), lines))

        if self.next is not None:
            if len(results) == 1:
                self.next.set_result(results[0])
            else:
                self.next.set_result(results)

            self.next = None
        else:
            if self.callback:
                for result in results:
                    self.callback(result)

    def send(self, message: str) -> Future:
        if self.transport is not None:
            self.next = self.loop.create_future()
            self.transport.write(bytes(message + "\r\n", "UTF-8"))
            return self.next
        else:
            future = self.loop.create_future()
            future.set_result(None)
            return future
