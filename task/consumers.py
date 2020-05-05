import json

from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
# from rabbitmq.recieve import consume
import pika
from redis_notifications import getDeclined, delDeclined


class AcceptTaskConsumer(AsyncConsumer):
    accepted = True
    first = True
    body = []

    def __init__(self, scope):
        super().__init__(scope)
        self.channel = self.connection.channel()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

    async def websocket_connect(self, event):
        print("AcceptTaskConsumer connected", event)
        await self.channel_layer.group_add(
            "delivery",
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        if event["text"] == "Hi":
            await self.get_task()
            if self.body is not None:
                await self.channel_layer.group_send(
                    "delivery",
                    {
                        "type": "message",
                        "text": json.dumps(self.body.pop().decode("utf-8"))
                    }
                )

    @sync_to_async
    def get_task(self):
        # while True:
        #     task_body = consume()
        #     if task_body is not None:
        #         return json.dumps(task_body.decode("utf-8"))

        self.channel.queue_declare(queue='task_', arguments={"x-max-priority": 3})

        self.channel.basic_consume(
            queue='task_', on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(body)
        self.body.append(body)
        # ch.stop_consuming()
        self.channel.stop_consuming()

    async def message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    async def websocket_disconnect(self, event):
        print(event)
        await self.send({
            "type": "websocket.close"
        })

# class DeclinedTaskConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("DeclinedTaskConsumer connected ", event)
#         await self.send({
#             "type": "websocket.accept"
#         })
#
#     async def websocket_receive(self, event):
#         print("Declined received ", event)
#         if event["text"] == "Hi":
#             declined = await self.getDec()
#             print("declined", declined)
#             await self.send({
#                 "type": "websocket.accept",
#                 "text": json.dumps(declined)
#             })
#
#             delDeclined()
#
#     async def websocket_disconnect(self, event):
#         print(event)
#         await self.send({
#             "type": "websocket.close"
#         })
#
#     @sync_to_async
#     def getDec(self):
#         while True:
#             x = getDeclined()
#             if x is not None:
#                 return x
