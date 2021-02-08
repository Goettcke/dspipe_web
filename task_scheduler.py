import pika, sys, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True)

#message = ' '.join(sys.argv[1:]) or "Hello Word!"
# The test user is -1
message = json.dumps({"user_id":0,
                      "algorithm": "knn_ldp",
                      "number_of_samples" : 5,
                      "dataset_name":"appendicitis",
                      "n_neighbors":10,
                      "quality_measure" : "accuracy",
                      "percent_labelled":50,
                      "alpha":0.2,
                      "gamma":20,
                      "kernel":"lp"})

channel.basic_publish(exchange="",
        routing_key="task_queue",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode = 2,
            ))
print(" [x] Sent %r " % message)
connection.close()
