from decouple import config
from app.models.product import Product
from app.models.db import get_session
import pika
import json

URL = config("URL")
params = pika.URLParameters(url=URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print('Received in main: ', data, '\n')
    if properties.content_type == 'product_created':
        product = Product(title=data['title'], image=product['image'])
        product.save(get_session())
        print('Product created')
    elif properties.content_type == 'product_updated':
        product = Product.objects.get(id=data['id'])
        product.title = data['title']
        product.image = data['image']
        product.save()
        print('Product updated')
    elif properties.content_type == 'product_deleted':
        product = Product.objects.get(id=data)
        product.delete()
        print('Product deleted')
    elif properties.content_type == 'product_viewed':
        print('Product viewed')
    else:
        print('No action for this type')


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)
print('Started Consuming Main')
channel.start_consuming()
channel.close()
