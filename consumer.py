import pika,json
from service2 import Product, db
#params=pika.URLParameters('http://adpubwco:5MlpDbbndBbZWMKZoMKNfuNMTvTBBSic@beaver.rmq.cloudamqp.com/adpubwco')
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost',heartbeat=600,blocked_connection_timeout=300))
channel=connection.channel()


channel.queue_declare(queue='serivce')
db.create_all()
def callback(ch,method,properties,body):
    print("[x] Received %r" %body)

    data=json.loads(body)
    print(data)
    if properties.content_type=="product_created":
        product=Product(id=data['id'],title=data['title'],image=data['image'])
        print(product)
        db.session.add(product)
        db.session.commit()

        print('Product created')

    elif properties.content_type=="product_updated":
        product=Product.query.get(data['id'])
        print(product)
        product.title=data['title']
        product.image=data['image']
        db.session.commit()
        print('product updated')

    elif properties.content_type=='product_deleted':
        product=Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product deleted')



channel.basic_consume(queue='service',auto_ack=True,on_message_callback=callback)
print('started Consuming')

channel.start_consuming()






'''


import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='service')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='service', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)'''