from typing import Union
from wmp import API


class Control:
    def __init__(self, connector):
        self.api = API(connector)

    async def get_id(self):
        return await self.api.id()

    async def get_state(self, ac_num: int):
        return await self.api.get(ac_num, "*")

    async def set_power(self, ac_num: int, state: str):
        return await self.api.set(ac_num, "ONOFF", state)

    async def get_power(self, ac_num: int):
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

    async def get_set_point(self, ac_num: int):
        result = await self.api.get(ac_num, "SETPTEMP")
        if result and result.function == "SETPTEMP":
            return result.value
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

    async def turn_on(self, ac_num: int):
        return await self.set_power(ac_num, "ON")

    async def turn_off(self, ac_num: int):
        return await self.set_power(ac_num, "OFF")

    async def set_mode_heat(self, ac_num: int):
        return await self.set_mode(ac_num, "heat")

    async def set_mode_cool(self, ac_num: int):
        return await self.set_mode(ac_num, "cool")

    async def set_mode_fan(self, ac_num: int):
        return await self.set_mode(ac_num, "fan")

    async def set_mode_dry(self, ac_num: int):
        return await self.set_mode(ac_num, "dry")
