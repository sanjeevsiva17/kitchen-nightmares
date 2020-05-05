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
    delivery = {}

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    async def websocket_connect(self, event):
        print("AcceptTaskConsumer connected", event)

        self.room_group_name = "delivery"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        if event["text"] == "Hi":
            await AcceptTaskConsumer.get_task()
            if AcceptTaskConsumer.body is not None:
                print(AcceptTaskConsumer.body)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "message",
                        "text": AcceptTaskConsumer.body[0]["body"]
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "message",
                        "text": "No New Tasks"
                    }
                )

        else:
            print(json.loads(event["text"])["id"])
            AcceptTaskConsumer.channel.basic_ack(delivery_tag=AcceptTaskConsumer.delivery[json.loads(event["text"])["id"]])
            AcceptTaskConsumer.delivery.pop(json.loads(event["text"])["id"])
            AcceptTaskConsumer.body.pop(0)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message",
                    "text": "No New Tasks"
                }
            )
            await AcceptTaskConsumer.get_task()
            if AcceptTaskConsumer.body is not None:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "message",
                        "text": AcceptTaskConsumer.body[0]["body"]
                    }
                )

    async def message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    @classmethod
    @sync_to_async
    def get_task(cls):
        # cls.connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))
        # cls.channel = cls.connection.channel()

        cls.channel.queue_declare(queue='task_', arguments={"x-max-priority": 3})

        cls.channel.basic_consume(
            queue='task_', on_message_callback=AcceptTaskConsumer.callback, auto_ack=False)
        cls.channel.start_consuming()

    @classmethod
    def callback(cls, ch, method, properties, body):
        task_obj = {"body": json.dumps(body.decode("utf-8")),
                    "delivery_tag": method.delivery_tag}
        AcceptTaskConsumer.body.append(task_obj)
        AcceptTaskConsumer.delivery[json.loads(json.loads(task_obj["body"]))["id"]] = method.delivery_tag
        cls.channel.stop_consuming()

    async def websocket_disconnect(self, event):
        print(event)
        await self.send({
            "type": "websocket.close"
        })

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

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
