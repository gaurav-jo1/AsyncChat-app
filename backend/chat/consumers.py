import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    print("Using the Websocket connection")

    def connect(self):
        self.accept()
        print("WebSocket connection established")

    def disconnect(self, close_code):
        print("WebSocket disconnected")

    def receive(self, text_data):
        print("Received raw text_data:", text_data)

        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

        print("Received JSON data:", text_data_json)

        message = text_data_json.get("message")

        if message:
            self.send(text_data=json.dumps({"message": message}))
        else:
            print("Invalid or missing 'message' key in JSON data")

