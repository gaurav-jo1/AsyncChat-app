import asyncio
import time

async def my_async_function(num:str):
    print(f"Inside async function {num}")
    # await asyncio.sleep(1)
    await time.sleep(1)
    print(f"Async function {num} completed")

async def main():
    print("Calling async function")
    await asyncio.gather (
        my_async_function(1), 
        my_async_function(2), 
    )
    print("Main ending")

# Run the event loop
asyncio.run(main())
