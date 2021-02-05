import pika, sys 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='35.234.71.178', port='5672'))

channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True) 

message = ' '.join(sys.argv[1:]) or "Hello Word!" 

channel.basic_publish(exchange="", 
        routing_key="task_queue",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode = 2,
            ))
print(" [x] Sent %r " % message) 
connection.close()
