import asyncio


async def main():    
    result = await bridge_a.call("add", 5, 10)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
