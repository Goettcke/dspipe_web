import pika, time
import json
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    message = json.loads(body)
    print(" [x] Received %r" % message)
    print(f" [x] algorithm is: {message['algorithm']}")
    user_id = message['user_id']
    algorithm = message['algorithm']
    number_of_samples = message['number_of_samples']
    dataset = message['dataset_name']
    quality_measure = message['quality_measure']
    percent_labelled = message['percent_labelled']

    docker_base = f"docker run --rm --name runner -v ~/runner_results/ds_pipe_runner/output:/app/output/ runner2"
    base_arguments = f"--user_id {user_id} --dataset_name {dataset} --quality_measure {quality_measure} --number_of_samples {number_of_samples} --percent_labelled {percent_labelled}"
    try:
        if algorithm == "knn_ldp":
            os.system(f"{docker_base} {base_arguments} --algorithm knn_ldp  --n_neighbors {message['n_neighbors']}")

        elif algorithm == "lp":
            if 'kernel' == "knn":
                os.system(f"{docker_base} {base_arguments} --algorithm lp --kernel knn --n_neighbors {message['n_neighbors']} ")
            else:
                os.system(f"{docker_base} {base_arguments} --algorithm lp --kernel knn --gamma {message['gamma']}")
        elif algorithm == "ls":
            if message['kernel'] == "knn":
                os.system(f"{docker_base} {base_arguments} --algorithm ls --kernel knn --n_neighbors {message['n_neighbors']}")
            else:
                os.system(f"{docker_base} {base_arguments} --algorithm ls --kernel knn --alpha {message['alpha']} --gamma {message['gamma']}")
        elif algorithm == "planetoid":
            pass
        else:
            ch.basic_nack(delivery_tag = method.delivery_tag)
    except:
        print("An error ocurred. Check the message, before continuing")


    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

