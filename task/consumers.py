import json

from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from rabbitmq.recieve import consume
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


class AcceptTaskConsumer(AsyncConsumer):
    accepted = True
    first = True

    async def websocket_connect(self, event):
        print("connected", event)
        await self.channel_layer.group_add(
            "delivery",
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        if event["text"] == "Hi":
            task = await self.get_task()
            print("here", task)
            await self.channel_layer.group_send(
                "delivery",
                {
                    "type": "message",
                    "text": task
                }
            )

    @sync_to_async
    def get_task(self):
        while True:
            task_body = consume()
            if task_body is not None:
                return json.dumps(task_body.decode("utf-8"))

    async def message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    async def websocket_disconnect(self, event):
        await self.send({
            "type": "websocket.close"
        })
