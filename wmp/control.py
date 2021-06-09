from typing import Union
from wmp.api import API


class Control:
    def __init__(self, api: API):
        self.api = api

    async def get_id(self):
        return await self.api.id()

    async def get_state(self, ac_num: int):
        return await self.api.get(ac_num, "*")

    async def set_power(self, ac_num: int, state: str):
        return await self.api.set(ac_num, "ONOFF", state)

    async def get_power(self, ac_num: int) -> Union[str, None]:
        result = await self.api.get(ac_num, "ONOFF")
        if result and result.function == "ONOFF":
            return result.value
        else:
            return None

    async def set_mode(self, ac_num: int, mode: str):
        return await self.api.set(ac_num, "MODE", mode)

    async def get_mode(self, ac_num: int):
        result = await self.api.get(ac_num, "MODE")
        if result and result.function == "MODE":
            return result.value
        else:
            return None

    async def set_set_point(self, ac_num: int, set_point: float):
        return await self.api.set(ac_num, "SETPTEMP", str(set_point))

    async def get_set_point(self, ac_num: int) -> Union[float, None]:
        result = await self.api.get(ac_num, "SETPTEMP")
        if result and result.function == "SETPTEMP":
            return float(result.value)
        else:
            return None

    async def set_fan_speed(self, ac_num: int, fan_speed: str):
        return await self.api.set(ac_num, "FANSP", fan_speed)

    async def get_fan_speed(self, ac_num: int) -> Union[str, None]:
        result = await self.api.get(ac_num, "FANSP")
        if result and result.function == "FANSP":
            return result.value
        else:
            return None
