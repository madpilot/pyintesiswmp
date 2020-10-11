from wmp import API


class Control:
    def __init__(self, api):
        self.api = api

    def set_power(self, ac_num, state):
        self.api.set(ac_num, "ONOFF", state)

    def get_power(self, ac_num):
        self.api.get(ac_num, "ONOFF")

    def set_mode(self, ac_num, mode):
        self.api.set(ac_num, "MODE", mode)

    def get_mode(self, ac_num):
        self.api.get(ac_num, "MODE")

    def set_set_point(self, ac_num, set_point):
        self.api.set(ac_num, "SETPTEMP", set_point)

    def get_set_point(self, ac_num):
        self.api.get(ac_num, "SETPTEMP")

    def set_fan_speed(self, ac_num, fan_speed):
        self.api.set(ac_num, "FANSP", fan_speed)

    def get_fan_speed(self, ac_num):
        self.api.get(ac_num, "FANSP")

    def turn_on(self, ac_num):
        self.set_power(ac_num, "ON")

    def turn_off(self, ac_num):
        self.set_power(ac_num, "OFF")

    def set_mode_heat(self, ac_num):
        self.set_mode(ac_num, "heat")

    def set_mode_cool(self, ac_num):
        self.set_mode(ac_num, "cool")

    def set_mode_fan(self, ac_num):
        self.set_mode(ac_num, "fan")

    def set_mode_dry(self, ac_num):
        self.set_mode(ac_num, "dry")
