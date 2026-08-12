import sys
import os
import asyncio

# Absolute baseline injection to guarantee modular lookups across local trees
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from python.pyjs import PyJS

# Initialize the bridge server on standard 127.0.0.1
bridge = PyJS()

# Scenario 1: A simple synchronous mathematical function
@bridge.register()
def basic_add(x: int, y: int) -> int:
    return x + y

# Scenario 2: An advanced asynchronous data processor with schema enforcement
@bridge.register(schema={"min_args": 2})
async def heavy_data_process(user_id: str, payload: dict) -> dict:
    print(f"[Demo Task] Processing heavy async operation for User: {user_id}")
    await asyncio.sleep(1) # Simulate real-world database or I/O lag
    return {
        "status": "PROCESSED",
        "processed_items": len(payload.get("items", [])),
        "system_telemetry": bridge.get_telemetry()
    }

if __name__ == "__main__":
    bridge.start()
