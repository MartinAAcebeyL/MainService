from decouple import config
import pika



URL = config("URL")
params = pika.URLParameters(url=URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print("-"*50)
    print('Received in main/consumer')
    print(body)
    print("-"*50)


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)
print('Started Consuming Main')
channel.start_consuming()
channel.close()
