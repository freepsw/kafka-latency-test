from confluent_kafka import Producer
from confluent_kafka import Consumer
import sys
import time
import base64
import logging
logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        img_path = "../data/" + str(sys.argv[1])
    else:
        img_path = "data/1mb.jpg"

    # img_path = "../data/10mb.jpg"
    image = open(img_path, 'rb')  # open binary file in read mode
    image_read = image.read()
    data = base64.b64encode(image_read)
    print("size 1: ", len(image_read))
    print("size 2: ", len(data))

    # broker = "freepsw-template-centos-4cpu-1:9092"
    broker = "kafka-test:9092"
    topic = "latency-test"
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    p = Producer({
            'bootstrap.servers': broker,
            'acks': 1,
            # 'socket.nagle.disable': True,
            'message.max.bytes': 15000000
           })

    conf = {
        'bootstrap.servers': broker,
        'group.id': 'my-group',
        'auto.offset.reset': 'latest',
        # 'socket.nagle.disable': True,
        # 'fetch.wait.max.ms': 0,
        # 'heartbeat.interval.ms': '1000',
        'message.max.bytes': 15000000
    }
    logger = logging.getLogger('consumer')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    logger.addHandler(handler)

    c = Consumer(conf, logger=logger)

    def print_assignment(consumer, partitions):
        print('Assignment:', partitions)
    c.subscribe([topic], on_assign=print_assignment)
    t41 = time.time()

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                             (msg.topic(), msg.partition(), msg.offset()))

    # data = b"some_message_bytes"
    for _ in range(20):
        try:
            t1 = time.time()
            p.produce(topic, data)
            t2 = time.time()
            print("1. Producer Send : ", t2 - t1)
        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                             len(p))

        # Serve delivery callback queue.
        # NOTE: Since produce() is an asynchronous API this poll() call
        #       will most likely not serve the delivery callback for the
        #       last produce()d message.
        # p.poll(0)
        # t3 = time.time()

        # Wait until all messages have been delivered
        sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
        # p.flush()
        # print("Producer 2 : ", t3 - t2)

        while True:
            msg = c.poll(20)

            if msg is None:
                print("None")
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            # print('Received message: {}'.format(len(msg.value())))
            break
        # msg = c.poll(10)
        # print('Received message: {}'.format(len(msg.value())))
        c.commit(asynchronous=False)
        t3 = time.time()
        print("2. Consumer Received: ", t3 - t2)
        print("3. Total Time : ", t3 - t1)
        print("\n")

    p.flush()
    c.close()