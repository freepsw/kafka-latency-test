# Sending a large message using async send function in kafka producer

## STEP 1. Setting Large Message Configuration 
- 아래와 같은 설정으로 broker를 실행한 후, producer로 메세지(5MB) 전송하면 정상적으로 대량의 데이터가 전송됨
- Producer에서 send 호출히 sync(broker에서 응답이 올때 까지 기다림) 설정
```
# Broker 
> config/server.properties
max.message.bytes=15000000

# Producer 
> config/producer.properties
max.request.size=15000000

# Consumer 
> config/consumer.properties
max.partition.fetch.bytes=20000000 #The maximum amount of data per-partition the server will return.
fetch.max.bytes	52428800 (50 MiB) #The maximum amount of data the server should return for a fetch request.
```


## STEP 2. Sending messages(5MB) using producer async configuration (acks = 0)
### Producer Code 
- 5mb 이미지 파일을 읽어서 base64로 변환한 후 전송한다. (변환된 base64 사이즈는 6.4MB로 증가)
- producer.py code 
```python 
from kafka import KafkaProducer
import time
from kafka.producer.kafka import log
import base64

img_path= "./data/5mb.jpg"
image = open(img_path, 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.encodebytes(image_read)
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         acks=0, # Async
                         max_request_size=15000000
                         )

producer.send('test2', image_64_encode)
producer.flush()
producer.close()
```

### Problems : message is not deliverd to broker 
- 위 코드를 실제로 실행해 보면, 별도의 오류는 발생하지 않는다. 
- 다만 kafka consumer에서 producer에서 전송된 데이터를 읽어오지 못한다. 
- 그래서 broker에 message가 저장되었는지 offset을 확인해 보면, 실제로 데이터가 producer에서 전송되지 않았다.  
```
> bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test2
1432
```

### Send 1mb message using async configuration (acks=0)
- 동일한 코드에서 메세지 사이즈만 1mb로 변경했는데, 
- async 모드에서 정상적으로 동작한다?


## STEP 3. Cause Analysis
- 왜 message size에 따라서 broker로 전달 에러가 발생하는가?
- producer는 broker로 데이터를 전달하기 위하여 TCP socket을 활용한다. 
- 이때 broker로 전달하기 위해서 socket buffer에 데이터를 쓰는데,
- 이 buffer size가 너무 작은 경우 위와 같은 오류가 발생함. 


### Socket Send Buffer (end_buffer_bytes) Full 
- Broker로 전송시에 tcp로 보내는 데이터 보다 더 빨리 buffer로 전송하는 경우 발생
- 보통 async(acks=0) 전송의 경우 응답 확인 없이 무조건 buffer에 메세지를 쓰게된다. 
- 이때 producer의 send_buffer_bytes는 131,072(128 KB)이라서 금방 buffer가 꽉 차게되고,
- kernel에서는 producer가 더 이상 buffer에 쓰지 않도록 한다(blocking). 
    - 이렇게 되면, 결국 broker에 전달되는 데이터를 쓰지 못하게되고, 
    - broker에 데이터를 전송하지 못하는 현상이 발생한다.


## STEP 4. Change Producer configuration 
- producer.py code 
```python 
from kafka import KafkaProducer
import time
from kafka.producer.kafka import log
import base64

img_path= "./data/5mb.jpg"
image = open(img_path, 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.encodebytes(image_read)
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         acks=0, # Async
                         send_buffer_bytes=5*1024*1024, # --> 설정 추가
                         max_request_size=15000000
                         )

producer.send('test2', image_64_encode)
producer.flush()
producer.close()
```
