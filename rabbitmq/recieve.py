import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# task_list = []
#
# def callback(ch, method, properties, body):
#     task_list.append(json.loads(body))
#     channel.stop_consuming()
#
# def task():
#     if len(task_list) > 0:
#         return task_list.pop(0)
#     else:
#         return None
#
# channel.basic_consume(
#     queue='task_', on_message_callback=callback, auto_ack=True)

# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()

def consume():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue='task_')
    if method_frame is not None:
        if method_frame.NAME == 'Basic.GetEmpty':
            connection.close()
            return None
        else:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            connection.close()
            return body
    else:
        return None

# print(consume())