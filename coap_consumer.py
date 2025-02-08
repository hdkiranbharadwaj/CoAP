import asyncio
from aiocoap import Context, Message, Code

async def observe_resource(uri):
    """Subscribe to a CoAP resource and print updates."""
    protocol = await Context.create_client_context()
    request = Message(code=Code.GET, uri=uri, observe=0)  # Subscribe to updates

    try:
        requester = protocol.request(request)
        async for response in requester.observation:
            print(f"Received {uri.split('/')[-1].capitalize()}: {response.payload.decode()}°")
    except Exception as e:
        print(f"Failed to fetch {uri}: {e}")

async def main():
    subscriptions = []
    
    print("Choose resources to observe:")
    print("1. Temperature")
    print("2. Humidity")
    print("3. Both")
    
    choice = await asyncio.to_thread(input, "Enter your choice (1/2/3): ")  # Make input non-blocking
    
    if choice == "1" or choice == "3":
        subscriptions.append(observe_resource("coap://localhost/temperature"))
    if choice == "2" or choice == "3":
        subscriptions.append(observe_resource("coap://localhost/humidity"))

    if subscriptions:
        await asyncio.gather(*subscriptions)
    else:
        print("No subscriptions selected. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
