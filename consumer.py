
import pika, json, os , django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")
django.setup()
from products.models import Product 

params = pika.URLParameters('amqps://ygtwdsgt:kWLjRwODAZ3IXAwwnZVdMTweoRRA6emB@cow.rmq2.cloudamqp.com/ygtwdsgt')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch,method,properties,body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes are increased.')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()