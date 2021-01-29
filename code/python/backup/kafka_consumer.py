from kafka import KafkaConsumer
import base64
from datetime import datetime
import time
import logging
# logging.basicConfig(level=logging.DEBUG)
consumer = KafkaConsumer(
    'latency-test',
     bootstrap_servers=['kafka-test:9092'],
     # bootstrap_servers=['skcc11n00142:9092'],
     auto_offset_reset='latest',
     enable_auto_commit=True,
     max_partition_fetch_bytes=15000000,
     group_id='my-group')

for message in consumer:
    # print("Start : ", datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))

    start = time.time()
    print("START : ", start)
    message = message.value
    print('size : {}'.format(len(message)))
    end = time.time()
    print("END : ", end)
    print("Processing time :", end - start)
    # # print('{}'.format(message))
    # size = len(message)
    # # print("Base64 size ", size)  #
    # # print("Consumer send time :", time.time() - start)
    # # print("End : ", datetime.utcnow().isoformat(sep=' ', timespec='milliseconds'))
    # image_64_decode = base64.decodebytes(message)
    # image_result = open('./data/result.jpg', 'wb')  # create a writable image and write the decoding result
    # image_result.write(image_64_decode)
    consumer.commit()