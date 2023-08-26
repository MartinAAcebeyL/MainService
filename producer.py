import pika
import json
from decouple import config

params = pika.URLParameters(config('URL'))
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',
                          routing_key='admin', body=json.dumps(body), properties=properties)
