import asyncio
import wmp


class Connector:
    def __init__(self, host, loop, callback=None):
        self._host = host
        self._loop = loop
        self._asyncio = wmp.Asyncio(loop, callback)
        self.attempts = 0

    async def connect(self):
        while True:
            try:
                await self._loop.create_connection(lambda: self._asyncio, self._host, 3310)
                self._asyncio.disconnection_callback = self._reconnect
                self.attempts = 0
                return
            except OSError:
                self.attempts += 1
                delay = 2 ** self.attempts
                await asyncio.sleep(delay)

    def _reconnect(self):
        asyncio.run_coroutine_threadsafe(self.connect(), loop=self._loop)

    def transport(self):
        return self._asyncio
