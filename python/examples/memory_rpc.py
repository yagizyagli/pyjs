import asyncio

from pyjs import Bridge
from pyjs.core.bridge.transport.memory import MemoryTransport


async def main():

    transport_a = MemoryTransport()
    transport_b = MemoryTransport()

    transport_a.connect_peer(transport_b)
    transport_b.connect_peer(transport_a)

    bridge_a = Bridge(transport_a)
    bridge_b = Bridge(transport_b)


    async def add(a, b):
        return a + b


    bridge_b.expose(
        "add",
        add,
    )


    await bridge_a.start()
    await bridge_b.start()


    result = await bridge_a.call(
        "add",
        5,
        10,
    )


    print("RESULT:", result)


    await bridge_a.stop()
    await bridge_b.stop()


if __name__ == "__main__":
    asyncio.run(main())
