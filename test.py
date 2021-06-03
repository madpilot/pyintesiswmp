import wmp
import asyncio


def callback(results):
    print("callback: " + results.function + " " + results.value)


loop = asyncio.get_event_loop()
connector = wmp.Connector('192.168.1.157', loop, callback)
control = wmp.Control(connector.transport())


async def get_id():
    while True:
        print("Running")
        id_result = await control.get_id()
        if id_result:
            print(id_result.rssi)

        power = await control.get_power(1)
        if power:
            print("Power " + power)

        set_point = await control.get_set_point(1)
        if set_point:
            print("Set Point " + str(set_point))

        fan_speed = await control.get_fan_speed(1)
        if fan_speed:
            print("Fan Speed " + fan_speed)

        mode = await control.get_mode(1)
        if mode:
            print("Mode " + mode)

        await asyncio.sleep(2)


loop.create_task(get_id())
loop.run_until_complete(connector.connect())
loop.run_forever()
loop.stop()


# reader, writer = await asyncio.open_connection('192.168.1.209', 3310)
