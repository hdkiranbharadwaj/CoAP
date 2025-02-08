import asyncio
import random
from aiocoap import Context, Message, Code, resource


class TemperatureResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.temperature = 25  # Initial temperature
        asyncio.get_event_loop().create_task(self.update_temperature())

    async def update_temperature(self):
        """Simulate temperature change every 2 seconds."""
        while True:
            self.temperature = round(20 + random.uniform(-5, 5), 2)  # Simulated temperature
            print(f"Updated Temperature: {self.temperature}°C")
            self.updated_state()  # Notify observers
            await asyncio.sleep(2)

    async def render_get(self, request):
        return Message(payload=str(self.temperature).encode())


class HumidityResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.humidity = 50  # Initial humidity
        asyncio.get_event_loop().create_task(self.update_humidity())

    async def update_humidity(self):
        """Simulate humidity change every 2 seconds."""
        while True:
            self.humidity = round(40 + random.uniform(-10, 10), 2)  # Simulated humidity
            print(f"Updated Humidity: {self.humidity}%")
            self.updated_state()  # Notify observers
            await asyncio.sleep(2)

    async def render_get(self, request):
        return Message(payload=str(self.humidity).encode())


async def main():
    root = resource.Site()
    root.add_resource(["temperature"], TemperatureResource())
    root.add_resource(["humidity"], HumidityResource())

    server = await Context.create_server_context(root)
    print("CoAP Server is running...")
    await asyncio.get_running_loop().create_future()  # Keeps the server running


if __name__ == "__main__":
    asyncio.run(main())
