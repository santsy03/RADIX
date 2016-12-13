import pika
host = '127.0.0.1'
creds = pika.PlainCredentials('username', 'password')
params = pika.ConnectionParameters(host)
conn = pika.AsyncoreConnection(params)
ch = conn.channel()
ch.queue_delete(queue='events_queue_dev')
ch.close()
conn.close()
