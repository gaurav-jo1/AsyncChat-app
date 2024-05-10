import asyncio
import time
from asgiref.sync import async_to_sync


async def my_async_function(num: str):
    print(f"Inside async function {num}")
    await asyncio.sleep(5)
    print(f"Async function {num} completed")


# def sync_function(num: str):
#     print(f"Inside sync function {num}")
#     time.sleep(5)
#     print(f"sync function {num} completed")


async def main():
    print("Calling async function")
    await asyncio.gather (
        my_async_function(5),
        my_async_function(3),
    )

    print("Main ending")


start_time = time.time()

# Run the event loop
asyncio.run(main())

end_time = time.time()

print(f"The time it took is {end_time - start_time}")
