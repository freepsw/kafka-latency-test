from kafka import KafkaProducer
import time
from datetime import datetime
from kafka.errors import KafkaError
from kafka.producer.kafka import log
import base64
import logging
# logging.basicConfig(level=logging.DEBUG)

import sys

if len(sys.argv) >= 2:
    img_path = "./data/" + str(sys.argv[1])
else:
    img_path= "../data/1mb.jpg"

print(img_path)
image = open(img_path, 'rb') #open binary file in read mode
# image = open('./data/3m.jpg', 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.encodebytes(image_read)
producer = KafkaProducer(
                         # bootstrap_servers='freepsw-template-centos-4cpu-1:9092',
                         bootstrap_servers='kafka-test:9092',
                         linger_ms=5,
                         acks=1, # After appending the message to the leader
                         max_request_size=15000000
                         )

# start = time.time()
# for _ in range(100):
#    producer.send('test', b'some_message_bytes')

# print ("Start : ", datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
# print("START : ", start)
# image_64_encode = b"some_message_bytes"
print("Size : ", len(image_64_encode))
for _ in range(1):
    start = time.time()
    print("START : ", start)
    future = producer.send('latency-test', image_64_encode)
    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=20)
    except KafkaError as ex:
        # Decide what to do if produce request failed...
        log.exception(ex)
        pass
    end = time.time()
    print("END : ", end)
    print("PROCESSING: ", end-start)
producer.flush()
# print (record_metadata.topic)
# print (record_metadata.partition)
# print (record_metadata.offset)
# print("producer send size :", len(image_64_encode))
# print("END : ", time.time())
# print("producer send time :", time.time() - start)
# print ("End : ", datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
producer.close


#producer.py