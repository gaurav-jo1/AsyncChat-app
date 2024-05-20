import asyncio
import json


class MyparentClass:
    async def send_name(self, content):
        print("Print the name")
        print(f"{type(content)}: {content}")


class SendName(MyparentClass):
    async def say_name(self, name):
        await super().send_name(content = await self.encode_json(name))

    async def calling_name(self):
        await self.say_name(
            {
                "type": "welcome_message",
                "message": "Welcome to the Gaurav Websocket Connection",
            }
        )

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)


# Create an asynchronous main function to run the async method
async def main():
    send_name_instance = SendName()
    await send_name_instance.calling_name()


# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
