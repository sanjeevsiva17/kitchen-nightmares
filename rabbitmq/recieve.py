# import pika
# import json
#
#
# def consume():
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#
#     while True:
#         method_frame, header_frame, body = channel.basic_get(queue='task_')
#         if method_frame is not None:
#             if method_frame.NAME == 'Basic.GetEmpty':
#                 connection.close()
#                 return None
#             else:
#                 channel.basic_ack(delivery_tag=method_frame.delivery_tag)
#                 connection.close()
#
#                 return body
#
#         else:
#             print("here")
#             return None
#
# print(consume())

import pika


class PikaClient():
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)



    def consume():

        this.channel.queue_declare(queue='task_', arguments={"x-max-priority": 3})

        channel.basic_consume(
            queue='task_', on_message_callback=callback, auto_ack=True)

        channel.start_consuming()



