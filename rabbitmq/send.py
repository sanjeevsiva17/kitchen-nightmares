import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

max_priority = 3

channel.queue_declare(queue='task_', arguments={"x-max-priority": max_priority})


def publish(message, priority):
    channel.basic_publish(
        properties=pika.BasicProperties(priority=priority),
        exchange='',
        routing_key='task_',
        body=json.dumps(message)
    )

# task_body_1 = {
#     "id": 1,
#     "title": "12345678",
#     "priority": "H",
#     "created_by": 1,
#     "is_active": True
# }
#
# task_body_2 = {
#     "id": 1,
#     "title": "12345678",
#     "priority": "M",
#     "created_by": 1,
#     "is_active": True
# }
#
# task_body_3 = {
#     "id": 1,
#     "title": "12345678",
#     "priority": "L",
#     "created_by": 1,
#     "is_active": True
# }


# publish(task_body_3, 3)
# publish(task_body_1, 3)
# publish(task_body_2, 2)


print(" [x] Sent 'Hello World!'")

