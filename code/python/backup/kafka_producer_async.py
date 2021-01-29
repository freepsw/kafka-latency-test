from kafka import KafkaProducer
import time
from datetime import datetime
from kafka.errors import KafkaError
from kafka.producer.kafka import log
import base64
import logging
logging.basicConfig(level=logging.DEBUG)

import sys

if len(sys.argv) >= 2:
    img_path = "./data/" + str(sys.argv[1])
else:
    img_path= "../data/1mb.jpg"

print(img_path)
image = open(img_path, 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.encodebytes(image_read)
producer = KafkaProducer(bootstrap_servers='freepsw-template-centos-4cpu-1.us-central1-a.c.ds-ai-platform.internal:9092',
                         # linger_ms=5,
                         acks=0, # Async
                         # batch_size=16384,
                         send_buffer_bytes=5*1024*1024,
                         max_request_size=15000000
                         )
# image_64_encode = b"some_message_bytes"
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)

for _ in range(1):
    start = time.time()
    print("START : ", start)
    # producer.send('test2', image_64_encode)
    future = producer.send('test2', image_64_encode).add_callback(on_send_success).add_errback(on_send_error)
    end = time.time()
    print("END : ", end)
    print("PROCESSING: ", end-start)

# print (record_metadata.topic)
# print (record_metadata.partition)
# print (record_metadata.offset)
# print("producer send size :", len(image_64_encode))
# print("END : ", time.time())
# print("producer send time :", time.time() - start)
# print ("End : ", datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
producer.flush()
producer.close()
