#http://adpubwco:5MlpDbbndBbZWMKZoMKNfuNMTvTBBSic@beaver.rmq.cloudamqp.com/adpubwco

import pika,json
#params=pika.URLParameters('http://adpubwco:5MlpDbbndBbZWMKZoMKNfuNMTvTBBSic@beaver.rmq.cloudamqp.com/adpubwco')
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost',heartbeat=600,blocked_connection_timeout=300))
channel=connection.channel()
channel.queue_declare(queue='admin')
def publish(method,body):
    properties=pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='admin',body=json.dumps(body),properties=properties)
print("[x] Sent from admin app'")

