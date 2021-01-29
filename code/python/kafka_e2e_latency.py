from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.structs import OffsetAndMetadata
import time
import base64
import sys
import socket
import struct
# https://www.it-swarm.dev/ko/python/kafka-%EC%A3%BC%EC%A0%9C%EC%9D%98-%ED%8C%8C%ED%8B%B0%EC%85%98%EC%97%90-%EB%8C%80%ED%95%9C-%EC%B5%9C%EC%8B%A0-%EC%98%A4%ED%94%84%EC%85%8B%EC%9D%84-%EC%96%BB%EB%8A%94-%EB%B0%A9%EB%B2%95%EC%9D%80-%EB%AC%B4%EC%97%87%EC%9E%85%EB%8B%88%EA%B9%8C/824203942/
if len(sys.argv) >= 2:
    img_path = "./data/" + str(sys.argv[1])
else:
    img_path= "data/1mb.jpg"

# img_path= "./data/10mb.jpg"
# print(img_path)
image = open(img_path, 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.b64encode(image_read)
print("size 1: ", len(image_read))
print("size 2: ", len(image_64_encode))
# print("type b64: ", type(image_64_encode))

broker = 'kafka-test:9092'
topic = "latency-test"
group_id = "my-group" + str(int(time.time()))
print("group : ", group_id)

producer = KafkaProducer(bootstrap_servers=broker,
                         linger_ms=0,
                         max_block_ms=60000*1024,
                         acks=1, # After appending the message to the leader
                         # batch_size=0,
                         # send_buffer_bytes= 3* 1024 * 1024,
                         # key_serializer=str.encode,
                         # value_serializer=str.encode,
                         # socket_options=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),
                         #                 (socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 0, 0))],
                         max_request_size=15000000
                         )

consumer = KafkaConsumer(
                         bootstrap_servers=[broker],
                         auto_offset_reset='latest',
                         enable_auto_commit=False,
                         request_timeout_ms= 30000,
                         # receive_buffer_bytes= 64*1204,
                         fetch_max_wait_ms=0, # Default: 500, instantly fetch
                         # socket_options=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1), (socket.SOL_SOCKET, socket.SO_KEEPALIVE, True), (socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 1))],
                         group_id=group_id)

tp = TopicPartition(topic, 0)
consumer.assign([tp])
consumer.seek_to_end(tp)

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

for _ in range(3):
    start = time.time()
    # print("P START : ", start)
    producer.send(topic, image_64_encode)
    # producer.flush()
    pend = time.time()
    print("Produce : ", pend - start)


    # for p in consumer.partitions_for_topic(topic):
    #     tp = TopicPartition(topic, p)
    #     print(tp)
    #     # consumer.assign([tp])
    #     print("t11")
    #     committed = consumer.committed(tp)
    #     consumer.seek_to_end(tp)
    #     last_offset = consumer.position(tp)
    #     print("topic: %s partition: %s committed: %s last: %s lag: %s" % (
    #     topic, p, committed, last_offset, (last_offset - committed)))

    msg = consumer.poll(6000,1)
    # msg = next(consumer)
    # print(msg)
    # Response format is {TopicPartiton('topic1', 1): [msg1, msg2]}
    size = 0
    for tp, messages in msg.items():
        for message in messages:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            print("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                                                 message.offset, message.key,
                                                 len(message.value)))
            consumer.commit({
                tp: OffsetAndMetadata(message.offset, None)
            })

    cend = time.time()
    print("Consume : ", cend - pend)
    print("Total Time Sec : ", cend - start)
    print("")
    metrics = consumer.metrics()
    # print(metrics)
    # consumer.commit()




producer.close()
consumer.close()