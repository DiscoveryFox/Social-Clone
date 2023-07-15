def process_message(ch, method, properties, body):
    # Perform the machine learning computations on the received task
    # ...

    # Acknowledge the message to RabbitMQ that it has been successfully processed
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages(worker_id):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare the queue for this worker
    queue_name = 'worker_queue' + worker_id
    channel.queue_declare(queue=queue_name)

    # Set the prefetch count to limit the number of unacknowledged messages per worker
    channel.basic_qos(prefetch_count=1)

    # Start consuming messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=process_message)

    # Start the consumer loop
    channel.start_consuming()
