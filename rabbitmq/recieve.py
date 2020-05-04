import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


def consume():
    while True:
        method_frame, header_frame, body = channel.basic_get(queue='task_')
        print(method_frame)
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
