import json
import asyncio
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from rabbitmq.recieve import consume
import pika


class AcceptTaskConsumer(AsyncConsumer):
    accepted = True
    first = True

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        if event["text"] == "Hi":
            task_obj = self.get_task()
            if task_obj is not None:
                await self.send({
                    "type": "websocket.send",
                    "text": task_obj
                })
            else:
                await self.send({
                    "type": "websocket.send",
                    "text": "No New Tasks"
                })


    async def websocket_disconnect(self, event):
        print("here", event)
        # raise StopConsumer()
        await self.send({
            "type": "websocket.close"
        })

    def get_task(self):
        task_body = consume()
        if task_body is not None:
            print(task_body)
            return json.dumps(task_body.decode("utf-8"))
        return None

# task_obj = self.get_task()
# if task_obj is not None:
#     print("here", task_obj)
#     await self.send({
#         "type": "websocket.send",
#         "text": task_obj
#     })
# else:
#     await self.send({
#         "type": "websocket.send",
#         "text": "No New Tasks"
#     })


