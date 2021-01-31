# apache kafka latency test (web rest api vs kafka-python vs confluenct kafka vs EndToEndLatency)

## Test the lantency for large image transmission using apache kafka  
- Apache Kafka를 이용하여 이미지 데이터를 얼마나 빠르게(with low latency) 전달 가능한지 성능 테스트 
- 최종 목적은 AI(ML/DL) 모델의 입력으로 대량의 실시간 영상/이미지 데이터를 전달하는 메세지 큐로 사용하기 위하여,
- Drone/제조공정 등의 장비에서 전송된 이미지를 얼마나 빨리 AI Model로 전달 할 수 있는지 확인하기 위함. 
- https://www.confluent.io/blog/configure-kafka-to-minimize-latency/

- 최근 vision model(cnn, resnet 등)이 많이 서비스되면서, 
- 사이즈가 큰 영상(이미지)를 효율적으로 모델에 전송하기 위한 기술로 apache kafka를 활용하고 있다.
    - AWS는 이미 Kineiss video stream을 통해서 영상을 스트리밍하는 서비스를 제공하고 있다. 
- 그래서 Kafka에서 이미지를 전송하는 간단한 테스트를 진행하였고,
- 이 과정에서 latency를 얼마나 줄여주는지를 확인해 보았다.(HTTP 프로토콜과 비교하여)

### [현재 까지 결론]
    - Apache Kafka는 대량의 요청 처리를 위한 throughtput에 최적화 된 솔루션임.
    - 현재는 producer의 몇가지 옵션만 조정하여 테스트한 결과이므로,
    - 잠정적인 결과이지만, kafka의 latency를 향상을 위해서는 많은 시도가 필요할 것 같음.
    - 즉, 단일 요청의 latency는 확실히 느리지만,
    - 대량의 처리를 기준으로 평균 latency를 비교하면 평균적인 latency는 많이 낮아짐. 


## PREREQUISITE 

### Server Spec
- 1 machine GCP(asia-northeast3-a) : CentOS 7
- 8 cpus, 32G Memory 
- hostname : kafka-test

### Software Spec 
- Apache Kafka (2.13-2.7.0)
- Python Library : kafka-python(v2.0.2), confluent-kafka(v1.5.0)
- Scala Library : kakfka client lib (org.apache.kafka.clients.*)


### Test Environment 
- Web Client  -----------(http)-----------------> Web Server 
- Producer    ----(tcp)--->  Kafka  ----(tcp)---> Consumer

### Test Scenario 
- Latency를 비교하기 위해서 REST API와 다양한 kafka library(python, java)를 활용함. 
    - 모든 테스트 케이스에서 데이터를 수신하는 로직에서 수신된 데이터를 file로 저장하는 로직은 제외함. 
    - Network를 통해서 데이터를 수신한 시간까지만 latency 시간으로 계산함. 
- 그림 추가 ()
- Scenario 0. Socket 통신 latency 측정 
- Scenario 1. REST API latency 측정 
- Scenario 2. kafka-python library latency 측정 
- Scenario 3. confluent-kafka library latency 측정 
- Scenario 4. Kafka EndtoEndLatency Class 실행 및 측정 


## STEP 1. Set the apache kafka configuration 
### Download apachd kafka 
```
> cd ~/
> sudo yum install -y java
> curl https://downloads.apache.org/kafka/2.7.0/kafka_2.13-2.7.0.tgz -o kafka_2.13-2.7.0.tgz
> tar -xzf kafka_2.13-2.7.0.tgz
> cd kafka_2.13-2.7.0
```

### Set the Configuration for test 
#### For external acccess 
```
> vi config/server.properties
listeners=PLAINTEXT://broker-hostname:9092
```

#### For processing the large message  (about 15M)
- https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/kafka_performance_large_messages.html
```
> vi config/server.properties
max.message.bytes=15000000
message.max.bytes=15000000

> vi config/producer.properties
max.request.size=15000000

> vi config/consumer.properties
max.partition.fetch.bytes=20000000 #The maximum amount of data per-partition the server will return.(19 MiB)
fetch.max.bytes=52428800  #The maximum amount of data the server should return for a fetch request.(default 50 MiB)
```

- Setting for Topic 
    - Topic 생성시 설정 옵션을 추가한다. 
    - flush.messages 
        - producer에서 전송받은 메세지를 disk에 쓰는(fsync) 주기(메세지 개수에 따라)를 설정한다. 
        - 아래처럼 1을 설정하면, 메세지가 전송될 때 마다 disk에 쓰는 작업을 하게되는데, 
        - 이는 전체 처리량 관점에서는 비효율적인 구성이다. (Latency test에 최적화된 설정)
        - https://kafka.apache.org/documentation/#topicconfigs_flush.messages
    - max.message.bytes
        - topic으로 전송 가능한 최대 message size를 설정한다. 
    ```
     --config max.message.bytes=15000000 --config flush.messages=1
    ```


#### [Error] producer 오류 (Timeout)
##### Error
- 
- kafka.errors.KafkaTimeoutError: KafkaTimeoutError: Timeout after waiting for 10 secs.
##### Solve 
- /etc/hosts에 listener명과 ip 주소를 추가 
```
35.222.98.xxx broker-hostname
```

## STEP 2. Run apache kafka (jmx enabled)

### Run Broker 
```
> cd ~/kafka_2.13-2.7.0

> bin/zookeeper-server-start.sh config/zookeeper.properties

> env JMX_PORT=9999 bin/kafka-server-start.sh config/server.properties
```

### Create topic (resize message size per topic)
- http://kafka.apache.org/documentation/#topicconfigs
- --bootstrap-server 설정시 고려사항
    - apache kafka를 외부에서 접속할 수 있도록 listeners를 설정한 경우에는 apache kafka가 설치된 host name을 입력해야 함. 
    - 외부 접속 설정이 없는 경우에는 localhost 또는 IP를 입력할 수 있다. 
    - 만약 listeners를 설정했는데 localhost/IP를 입력하면 아래와 같은 오류 발생 
        - "Caused by: org.apache.kafka.common.config.ConfigException: No resolvable bootstrap urls given in bootstrap.servers"

```
> cd ~/kafka_2.13-2.7.0

> bin/kafka-topics.sh --bootstrap-server kafka-test:9092 --create --topic latency-test --partitions 1 \
  --replication-factor 1 --config max.message.bytes=15000000 --config flush.messages=1

# alter topic configuration if needed
> bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name test \
    --alter --add-config max.message.bytes=15000000
```

### Describe topic 
- https://gist.github.com/ursuad/e5b8542024a15e4db601f34906b30bb5
```
> cd ~/kafka_2.13-2.7.0
> bin/kafka-topics.sh --list --zookeeper localhost:2181

> bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic latency-test
Topic: test2	PartitionCount: 1	ReplicationFactor: 1	Configs: max.message.bytes=15000000,flush.messages=1
	Topic: test2	Partition: 0	Leader: 0	Replicas: 0	Isr: 0


> bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list kafka-test:9092 --topic latency-test --time -1 --offsets 1 | awk -F ":" '{sum += $3} END {print sum}'

# check offset per partitoin
# time_option : -1 (latest), -2 (earliest)
## latest : 가장 마지막에 도착한 message의 offset (producer에서 10개를 보냈다면 10개가 보임)
## earliest : 가장 먼저 도착한 message의 offset(일반적으로 0, 그런데 retention 정책으로 message가 삭제되었다면, 삭제된 이후의 offset이 출력됨)
> bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list kafka-test:9092 --topic latency-test --time -1
latency-test:0:8302

> bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list kafka-test:9092 --topic latency-test --time -2
latency-test:0:0


# Check Lag 
> bin/kafka-consumer-groups.sh --bootstrap-server kafka-test:9092 --list
test-consumer-group
> bin/kafka-consumer-groups.sh  --describe  --group test-consumer-group  --bootstrap-server kafka-test:9092 
Consumer group 'test-consumer-group' has no active members.

GROUP               TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID     HOST            CLIENT-ID
test-consumer-group latency-test    0          8302            8302            0               -               -
```
    

## STEP 3. Run producer and consumer console for checking the kafka
### Download data
```
> cd ~/
> curl https://upload.wikimedia.org/wikipedia/commons/1/16/AsterNovi-belgii-flower-1mb.jpg -o 1mb.jpg (1mb)
```

### Run Consumer Console 
```
> cd ~/kafka_2.12-2.5.0
> bin/kafka-console-consumer.sh --bootstrap-server kafka-test:9092 \
  --consumer.config config/consumer.properties --topic latency-test --from-beginning
```


### Run Producer Console 
- 테스트 용도로 실행 (실제 테스트는 python, java sdk를 활용)
- 실행 후 kafka-console-consumer에 binary 데이터가 출력되는지 확인해 본다. 
```
> cd ~/kafka_2.12-2.5.0
> bin/kafka-console-producer.sh --broker-list kafka-test:9092 \
  --topic latency-test  --producer.config config/producer.properties < ~/1mb.jpg
```

## STEP 4. Run the test application to check end to end latency for sending image file 
- 1.3mb 이미지 파일을 client(producer, web client)에서 보내고 server(consumer, web server)에서 수신하는데 걸리는 전체 시간을 측정
- 각 시나리오 별로 20번을 전송하고, 평균적인 소요시간을 측정함. 
- 이때 kafka의 경우 producer에서 전송하는 시간과 consumer에서 수신하는 시간을 분리하여 확인한다. 
### Create virtuan env for python version 3
```
> sudo yum update -y
> sudo yum install -y  yum-utils
> sudo yum install -y python3 git

> cd ~
> git clone https://github.com/freepsw/kafka-latency-test.git
> cd ~/kafka-latency-test/code/python
> python3 -m venv python3-virtualenv
> source python3-virtualenv/bin/activate
> pip install -r requirements.txt
```

### Test scenario 0. Send a 1.3 mb image file using socket protocol 

#### Compile java code 
```
> cd ~/kafka-latency-test/code/java/socket-examples/src
> javac -cp . SocketClient.java
> javac -cp . SocketServer.java
```

#### Run socket server
- Socket server에서 전송된 이미지 파일을 File로 저장하는 부분은 제거함. 
- Disk i/o 시간은 테스트트에서 제외
```
> cd ~/kafka-latency-test/code/java/socket-examples/src
> java SocketServer 
Socket server has started....

```

#### Send image file to socket server

```
> cd ~/kafka-latency-test/code/java/socket-examples/src
> java SocketClient
Elapsed Time: 0.018 : 18.0
Elapsed Time: 0.002 : 2.0
Elapsed Time: 0.002 : 2.0
Elapsed Time: 0.001 : 1.0
Elapsed Time: 0.002 : 2.0
Elapsed Time: 0.002 : 2.0
Elapsed Time: 0.003 : 3.0
Elapsed Time: 0.001 : 1.0
```

### Test scenario 1. Send a 1.3 mb image file using REST API
#### Run the web server 
```
> cd ~/kafka-latency-test/code/python
> python web_server.py
```

#### Send a 1mb image file to web server 20 times
```
> python web_client.py
image binary size  1302245
PROCESSING TIME:  0.006935834884643555
PROCESSING TIME:  0.003009319305419922
PROCESSING TIME:  0.0022058486938476562
.....
```

### Test scenario 2. Send a 1.3 mb image file using python library (kafka-python)
#### Run the test application
```
> cd ~/kafka-latency-test/code/python
> python kafka_e2e_laency.py

Produce :  0.003731966018676758
latency-test:0:16896: key=None value=1736328
Consume :  0.5665855407714844
Total Time Sec :  0.5703175067901611

Produce :  0.002213716506958008
latency-test:0:16897: key=None value=1736328
Consume :  0.6164145469665527
Total Time Sec :  0.6186282634735107

......
```

#### Procuder & Consumer confiuration
```python
producer = KafkaProducer(bootstrap_servers=broker,
                         linger_ms=0,
                         max_block_ms=60000*1024,
                         acks=1, # After appending the message to the leader
                         max_request_size=15000000
                         )

consumer = KafkaConsumer(
                         bootstrap_servers=[broker],
                         auto_offset_reset='latest',
                         enable_auto_commit=False,
                         request_timeout_ms= 30000,
                         fetch_max_wait_ms=0, # Default: 500, instantly fetch
                         group_id=group_id)
```

### Test scenario 3. Send a 13. mb(1302245 bytes) image file using python library (kafka-python)
#### 입력 인수 설명 
    - broker list : kafka broker의 주소:port
    - topic name : 테스트할 topic name (latency-test)
    - num_message : 몇개의 메세지를 연속적으로 보낼 것인지 (여기서는 20개)
    - producer_acks : producer 전송시 옵션 (1, 원본만 저장후 결과 리턴)
    - message_size_bytes : 보낼 메세지 1개의 사이즈 (1.3mb 이미지의 사이즈 지정)

#### Edit the EndToEndLatency.scala to log each processing time and build the code.

```
# 1. Install necessary libraries to build kafka source code.
> yum install -y git wget unzip 
> wget https://downloads.gradle-dn.com/distributions/gradle-6.8-bin.zip
> unzip gradle-6.8-bin.zip
> mv gradle-6.8 /usr/local/gradle
> sudo vim /etc/profile.d/gradle.sh
export PATH=/usr/local/gradle/bin:$PATH

> source /etc/profile.d/gradle.sh

# java compile에 필요한 jdk library를 위해서 아래 jdk-devel 버전을 추가로 설치해야 한다. 
> yum install -y  java-1.8.0-openjdk-devel
> vi ~/.bash_profile
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64


# 2. Download source code and set the configurations to send large message 
> git clone https://github.com/apache/kafka.git
> cd kafka
> vi config/producer.properties
max.request.size=15000000


# 3. Edit the source code
#    produce time, consume time, total time으로 구분하여 처리 시간을 기록
> vi core/src/main/scala/kafka/tools/EndToEndLatency.scala
      val produce_time = System.nanoTime
      //println("Produce Time : " + (produce_time - begin)/1000/1000/1000.toFloat)

      val recordIter = consumer.poll(Duration.ofMillis(timeout)).iterator

      val consume_time =  System.nanoTime

      println("Produce Time : Consume Time = " + (produce_time - begin)/1000/1000/1000.toFloat + "," + (consume_time - produce_time)/1000/1000/1000.toFloat)

      latencies(i) = elapsed / 1000 / 1000
      println("Processing Time : " + latencies(i)/1000.toFloat)  // <-- 개별 message 처리 시간 기록 (seconds)


# 4. Build kafka source code.
> gradle
> ./gradlew clean
> ./gradlew jar

# 5. Run the test.
> bin/kafka-run-class.sh kafka.tools.EndToEndLatency kafka-test:9092 latency-test 20 1 1302245 config/producer.properties

Produce Time : Consume Time = 0.081,0.039
Processing Time :0.122
Produce Time : Consume Time = 0.023,0.013
Processing Time :0.037
Produce Time : Consume Time = 0.021,0.012
Processing Time :0.034
.......
Avg latency: 38.5564 ms

Percentiles: 50th = 34, 99th = 122, 99.9th = 122
```
- 테스트 결과를 보면, 제일 처음 전송할 때만 111ms이고, 50%는 34ms 이내에 처리된다. 

#### Procuder & Consumer confiuration
- 여기에 없는 설정은 Apache Kafak 기본 설정을 따른다. 
```scala
    consumerProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false")
    consumerProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest")
    consumerProps.put(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG, "0") //ensure we have no temporal batching

    producerProps.put(ProducerConfig.LINGER_MS_CONFIG, "0") //ensure writes are synchronous
    producerProps.put(ProducerConfig.MAX_BLOCK_MS_CONFIG, Long.MaxValue.toString)
    producerProps.put(ProducerConfig.ACKS_CONFIG, producerAcks.toString)
```


## STEP 5. Test Result 
### ALL Test Result 
- REST API/Socket 통신이 가장 빠르게 데이터를 전달하며, 
- python (kafka-python library)를 사용한 케이스가 최악의 성능을 보인다.

![Test Result All](/images/01.result_all.png)


### Top3 Test Result 
- 가장 속도가 느린 테스트 케이스를 제외하고, 
- 나머지 e2e latency를 비교함. 
- python-confluent가 rest api의 속도에 어느정도 비슷한 성능을 유지함. 
![Test Result Top3](/images/02.result_top3.png)

### Producer vs Consumer Latency
- Kafka의 성능 구간을 크게 produce, consume으로 구분하였을때 
- 어느 구간에서 가장 많은 시간이 소요되는지 확인해 보면, 
- Producer 구간의 처리 속도가 전체 성능에 많은 영향을 미치는 것을 볼 수 있다. 
- 즉, Kafka로 데이터를 전달하는 주기를 빠르게 조정하는 설정을 확인해야 한다. 
    - 하지만, latency를 최적화하면 throughtput이 너무 낮아질 수 있으므로, 
    - 이를 업무 목적에 맞게 조정할 필요가 있음. 

![python confluent latency](/images/10.result_python-confluent.png)


![java latency](/images/11.result_java_e2e.png)


### 그럼 kafka-confluent library는 어떤 설정이 다를까?
- 아래 3개의 library에 기본으로 설정된 값을 비교해 보면, 
- 크게 차이가 나지 않으며, 실제 다른 값들을 조정해 봐도 성능(latency)가 크게 줄어들지 않았다. 
- 그럼 kafka-confluent library만 제공하는 다른 설정이 있는걸까?

#### Compare the configutation value of each kafka library
- 개별 라이브러리에서 기본으로 제공하는 configuration을 비교
    - kafka-confluent : https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    - python-kafka : https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
- 설정값의 차이는 크지 않음.

```
|  python-kafka   | python-confluent  |   java

fetch_min_bytes                          | 1               | 1                 |  1                                                                                         
fetch_max_wait_ms                        | 500             | 500               |  500                                                                    
fetch_max_bytes                          | 52,428,800      | 52,428,800        |  52,428,800                                                                                
max_partition_fetch_bytes                | 1,048,576       | 1,048,576         |  1,048,576                                                                                        
request_timeout_ms                       | 305,000         | 30,000            |  30,000                                                                            
retry_backoff_ms                         | 100             | 100               |  100                                                                   
reconnect_backoff_ms                     | 50              | 100               |  50                                                                      
reconnect_backoff_max_ms                 | 1000            | 10,000            |  1,000                                                                             
max_in_flight_requests_per_connection    | 5               | 1,000,000         |  ??                                                                                            
auto_offset_reset                        | latest          | latest            |  latest                                                                         
enable_auto_commit                       | TRUE            | TRUE              |  TRUE                                                                        
auto_commit_interval_ms                  | 5000            | 5,000             |  5,000                                                                           
check_crcs                               | TRUE            | FALSE             |  -                                                                
metadata_max_age_ms                      | 300,000         | 900,000           |  -                                                                               
partition_assignment_strategy            | RangePartitionA | -                 |  ?                    
max_poll_records                         | 500             | 300,000           |  500                                                                     
max_poll_interval_ms                     | 300000          | 10,000            |  300,000                                                                           
session_timeout_ms                       | 10000           | 3,000             |  10,000                                                                       
heartbeat_interval_ms                    | 3000            | -                 |  3,000                                                                      
receive_buffer_bytes                     | 32,768          | -                 |  65,536          <-- confluent는 0으로 설정하여, 시스템 디폴트를 사용하도록 함 (변경 적용해 봤으나, 별 차이 없음)                                                                
send_buffer_bytes                        | 131,072         | -                 |  131,072         <-- confluent는 0으로 설정하여, 시스템 디폴트를 사용하도록 함 (변경 적용해 봤으나, 별 차이 없음)                                                              
socket_options                           |                 | -                 |  -                                                         
consumer_timeout_ms                      | forever         | -                 |  -                                                                    
security_protocol                        | PLAINTEXT       | -                 |  PLAINTEXT                                                                     
ssl_check_hostname                       | TRUE            | -                 |  -                                                                
connections_max_idle_ms                  | 540000          | -                 |  540,000                                                                        
metrics_sample_window_ms                 | 30000           | -                 |  30,000                                                                        
metrics_num_samples                      | 2               | -                 |  2                                                               
metrics.recording.level                  |                 | -                 |  -                                                                 
check_crcs                               | TRUE            | -                 |  10,000                                                         
socket.connection.setup.timeout.ms       |                 | -                 |  127,000                                                                             
socket.connection.setup.timeout.max.ms   |                 | -                 |  2                                                                                 
rebalance.timeout.ms                     |                 | -                 |  TRUE                                                               
TCP_NODELAY                              | TRUE            | -                 |  -                  

```

#### kafka-confluent library만의 세부 설정 값들
- kafka-confluent의 latency가 더 빠르게 처리할 수 있도록 영향을 줄 수 있는 설정값 확인 필요



# [ETC]

## 1. File Encoding Type 관련 정리 
- 이미지 파일(binary)을 네트워크로 전달하려면, 파일을 전송 가능한 방식으로 변환해야 한다. 
- 이미지 파일은 자체 압축기능이 있어서, 이를 binary로 형태로 바로 전송하는 것이 효과적이다. 
- 그래서 base64를 사용한다. 

### Byte array
- 이미지 파일 binary를 그대로 전달하려면 이미지의 내용을 byte array로 변환하여 바로 전달 가능
- 그런데, Byte array로 변환된 사이즈를 확인해 보면, 거의 10배 까지 크기가 증가된다. 
    - 왜내하면, 이미지 포맷은 자체 압축이 적용되어 파일을 최적화 하여 저장하는데, 
    - 이를 byte로 변환하게 되면서 압축을 전혀 적용할 수 없게 되는 것이다. 
    - 실제 1.3M 정도의 jpg 이미지를 byte로 변환하여 크기를 측정해 보면 40M 까지 증가한다. 
    - https://stackoverflow.com/questions/20420971/image-size-increased-if-image-convert-to-byte-array

### Base64 
- 이미지의 원본 binary(압축된 형태 그대로)를 text로 변환해 주는 인코딩 방식
    - https://www.base64decode.org/
    - https://en.wikipedia.org/wiki/Base64
- 왜 base64를 사용하는가?
    - 전송 측의 character set과 수신 측의 character가 공통으로 인식할 수 있는 있도록,
    - 문자열과 상관없는 ASCII문자열(A-Z, a-z, 0-9, 2개문자)로만 구성된 인코딩 방식이다. 
    - 즉, 인터넷과 같이 누구나 데이터를 주고 받는 환경에서 binary르 데이터를 표준화된 방식으로 송/수신하기 위한 방식
- 왜 base 64를 사용하면 파일 사이즈가 커지는가?
    - base64는 binary 데이터를 6bit 단위로 하나의 문자로 변환한다. (기존은 8bit)
    - 그래서 원래 3글자(Man)이라는 단어는 8bit*3 = 24bit인데, (1byte = 8bit)
    - 이를 6bit로 변환하면 24 bit / 6 bit = 4글자로 증가하게 된다. 
    - 또한 문자열이 6bit로 분할 되지 않을 경우, 나머지 빈 공간을 padding 문자로 채우게 된다. 
        - 예를 들어 many라는 단어 (32bit)를 base64로 변환하기 위해 6bit로 나누면,
        - 5단어 (32/6 = 5단어 + 2bit)외에 추가 2bit가 남게 되는데, 이를 padding으로 채운다는 의미
    - 그래서 base64로 인코딩 하면, 대략 33% 정도 크기가 증가한다. 

## 2. 실제 apache kafka 운영 환경에서 고려해야 할 설정들 
- 실제 운영환경에서 Kafka에서 고려할 설정들
- https://kafka.apache.org/08/documentation.html
### Broker Configuration 
- disk flush rate 
    - 처리량 관점에서는 너무 잦을 수록 성능이 낮아짐 (disk에 쓰는 속도)
    - latency 관점에서는 빨리 자주 써야 응답이 빨라짐 
### Producer Configration 
- compresssion
- sysnc vs asyc send
- batch size (for async producer ???)

### Consumer Configuration 
- fetch size 

### Broker Configurations Examples (실제 운영환경에서 권장)
``` conf
# Replication configurations
num.replica.fetchers=4
replica.fetch.max.bytes=1048576
replica.fetch.wait.max.ms=500
replica.high.watermark.checkpoint.interval.ms=5000
replica.socket.timeout.ms=30000
replica.socket.receive.buffer.bytes=65536
replica.lag.time.max.ms=10000
replica.lag.max.messages=4000

controller.socket.timeout.ms=30000 # The socket timeout for commands from the partition management controller to the replicas.
controller.message.queue.size=10 # The buffer size for controller-to-broker-channels

# Log configuration
num.partitions=8    # default 1
message.max.bytes=1000000
auto.create.topics.enable=true
log.index.interval.bytes=4096
log.index.size.max.bytes=10485760
log.retention.hours=168
log.flush.interval.ms=10000
log.flush.interval.messages=20000
log.flush.scheduler.interval.ms=2000
log.roll.hours=168
log.retention.check.interval.ms=300000
log.segment.bytes=1073741824

# ZK configuration
zk.connection.timeout.ms=6000
zk.sync.time.ms=2000

# Socket server configuration
num.io.threads=8 # The number of I/O threads that the server uses for executing requests. You should have at least as many threads as you have disks.
num.network.threads=8 # Default 3, The number of network threads that the server uses for handling network requests. 
socket.request.max.bytes=104857600 # The maximum request size the server will allow. This prevents the server from running out of memory and should be smaller than the Java heap size.
socket.receive.buffer.bytes=1048576 # Default 100KB(100*1024), The SO_RCVBUFF buffer the server prefers for socket connections
socket.send.buffer.bytes=1048576
queued.max.requests=16
fetch.purgatory.purge.interval.requests=100
producer.purgatory.purge.interval.requests=100
```

### Configuration 상세 확인
#### Socket 설정 
- https://stackoverflow.com/questions/4257410/what-are-so-sndbuf-and-so-rcvbuf 참고

- socket.request.max.bytes (Default 100MB, 100 * 1024 * 1024) 
    - Broker 서버가 수신 가능한 최대 요청 사이즈 
    - 이 값은 Java heap 크기를 넘지 않도록 설정해야 Out of Memory가 발생하지 않음.
    - 크게 할수록 한번에 많은 요청을 받는건가?
    - producer/consumer 모두에게 적용 (둘다 request 실행)

- socket.receive.buffer.bytes (100KB, 102400 = 100 * 1024) 
    - socket connection에서 SO_RCVBUFF buffer 사이즈
    - SO_RCVBUFF란?
        - socket에 데이터를 수신한 후, 이를 socket에 연결된 process가 읽어간 시간 동안
        - 데이터를 보관할 사이즈를 의미.
        - 즉, 너무 작으면 프로세스가 전부 가져가기 전에 buffer가 꽉 차게 되면서, 더 이상 데이터를 수신하지 못하거나 조금씬 수신하게 됨. 
            - TCP : buffer가 꽉 차면, sender에게 데이터를 조금씩 보내라고 전달
            - UDP : buffer가 꽉 차면, 이후에 들어오는 데이터는 유실(버림)
        - 그래서 운영환경에서는 이를 1024 * 1024 (1MB)로 확장 

- socket.send.buffer.bytes (100KB, 102400 = 100 * 1024) 
    - socket connection에서 SO_SNDBUFF buffer 사이즈
    - SO_SNDBUF 란?
        - TCP에서 데이터를 외부(remote)로 전송하기 위해서 임시로 저장하는 buffer 사이즈
            - UDP는 전송된 데이터에 대한 체크를 하지 않으므로, 
            - 전송후에는 결과와 상관없이 buffer를 비우게 된다. 
        - 만약, 이 buffer가 꽉 차게 되면, kernel에서 이를 감지하게 되고,
        - 프로세스가 더 이상 이 buffer로 데이터를 전송하지 않도록 한다(blocking). (대신 local buffer로 전달)
        - 이후 buffer가 비워지면(네트워크로 전송되면) blocking을 해제하고, buffer에 데이터를 쓰도록 한다. 
        - 이 buffer가 꽉 차는 또다른 경우는
            - 전송된 데이터에 대한 ack를 받지 못하는 경우(네트워크 오류 등으로), buffer가 비워지지 못하고 꽉 차게된다.
    - Producer 관점 고려사항
        - Broker로 전송시에 tcp로 보내는 데이터 보다 더 빨리 buffer로 전송하는 경우 고려
        - 보통 async(acks=0) 전송의 경우 응답 확인 없이 무조건 buffer에 메세지를 쓰게된다. 
        - 이때 producer의 send.buffer.bytes는 131,072(128 KB)이라서 금방 buffer가 꽉 차게되고,
        - kernel에서는 producer가 더 이상 buffer에 쓰지 않도록 한다(blocking). 
            - 이렇게 되면, 결국 broker에 전달되는 데이터를 쓰지 못하게되고, 
            - broker에 데이터를 전송하지 못하는 현상이 발생한다.

    kafka에서는 consumer가 가져갈 데이터를 선택(offset의 범위만큼)하기 때문에,
    - 이 buffer가 꽉 차는 경우가 많이 발생하게 되는지 판단하기 어렵다. 


#### Request Purgatory 설정 
- https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=34839465
- 특정 조건(성공 또는 실패)을 만족할 때 까지 request(요청)을 대기(격리)하는 것
- 2개의 요청(produce, fetch)에 대해서 purgatory가 적용됨 
##### 요청에 대해서 purgatory를 적용하는 이유는?
- consumer의 long fetch 요청을 지원 (예를 들어, broker에 데이터가 없는 경우 반복적인 요청을 방지한다)
- producer의 전송과 fetch의 응답 조건이 만족할 때 까지 요청 큐를 채우고, 불필요한 netork thread를 차단(block)한다. 
    - 즉, producer의 요청이 왔더라도, 특정 조건이 만족 될때 까지 요청을 큐에 저장하고
    - 특정 조건을 만족할 때 한번에 요청 큐에 있는 요청들을 처리 한다. 
    - 아마도 throughput을 향상하기 위한 방법 --> 반대로 말하면 latency를 떨어트리는 요인  
##### 그럼 어떤 조건을 만족해야 하는가?
- producer, fetch(consumer) 각각 언제 purgatory 추가/삭제에 대한 조건을 가짐
- ProducerRequestPurgatory, FetchRequestPurgatory 에 상세 조건이 명시됨 (코드를 봐야함)

##### 어떻게 동작하는가? (flow)
- 1. producer/consumer에서 요청이 도착하게 되면, purgatory에 격리되어야 하는지 조건부터 확인
- 2. request counter 증가
    - 새로운 요청이 추가될 경우 purgatory의 요청 건수를 증가 시킴 (*.purgatory.purge.interval.requests)
- 3. 해당 요청이 watcher poll에 등록
    - 등록할 때 (topic, parition) 튜플을 키로 등록함. 
    - watcher는 요청한 작업이 완료되었는지 확인하는 역할을 함. 
    - 동일한 튜플 키를 가진 요청이 추가되는 경우, 해당 튜플의 키를 가진 모든 요청의 작업을 검사한다. 
- 4. 요청이 특정 시간 동안 처리되지 못하는 경우(expired), request reaper thread가 요청 큐에서 제거
    - delay된 요청들을 참조하는 2개의 컴포넌트가 있는데, 
    - 하나는 purgatory's watcher이고, 
    - 두번째는  request reaper이다. 
    - 따라서, 요청이 다 처리되면(satisfied), 최종적으로 위 2개의 컴퍼넌트로 부터 제거될 것이다.  

##### Request Reaper Thread 란?
- 요청 큐에 등록된 요청 중에서 대기 시간(deadline)을 넘긴 요청을 찾아서 제거/만료(expire)하는 역할을 수행
- 먼저 expired된 요청을 찾아서, purgatory's expire method를 통해서 처리한 후, 
- client에게 처리된 결과를 전달한다. (요청 만료)
- 이러한 expired 요청들은 satisfied 요청으로 변경되고, 최종적으로 purgatory에거 제거된다. 
- 그럼 언제 Request Reaper Thread가 동작하는가?
    - *.purgatory.purge.interval.requests 값을 확인 (default 10,000)
    - purgatory에서 대기중인 요청 개수가 위의 설정값에 도달하면, 요청 큐에 있는 모든 요청을 검사하고,
    - 된 요청이 있는지 확인하고 제거한다. 

##### requests handling
###### Producer
- 요청이 언제 purgatory에 추가되는가? (요청이 격리/지연 되는가?)
    - Producer에서 ack=-1 (모든 복제 완료 후 요청에 대한 응답을 처리하는 경우)
- 언제 요청이 expired 되는가?
    - producer의 요청이 대기 시간을 초과하는 경우 (request.timeout.ms)
    - client에게 expired 된 요청에 대한 응답을 전송 (요청 대기 시간 초과 등..)
- 언제 요청이 satisfied 되는가?
    - follwer가 빠르게 leader의 데이터를 복제 완료한 경우 (요청이 정상 처리됨)

###### Consumer 
- 요청이 언제 purgatory에 추가되는가?
    - fetch.wait.max.ms is 0 (default 100)
        - broker에 충분한 데이터(fetch.min.bytes)가 없는 경우, broker가 consumer의 요청을 격리 시키는 시간 
        - 한번의 요청에 더 많은 데이터를 처리하기 위한 용도
    - fetch.min.bytes (default 1) 보다 적은 데이터가 broker에 도착한 경우 (1byte가 될때 까지 기다람)
        - 이렇게 요청을 격리하고, 바로 응답하지 않으면
        - consumer는 데이터가 왔는지 체크하기 위해서 계속 요청(long polling)을 할 필요가 없어서 효율성 향상
- 언제 요청이 expired 되는가?
    - consumer가 fetch.wait.max.ms 만큼 기다린 이후 (time out)
- 언제 요청이 satisfied 되는가?
    - fetch.min.bytes 이상의 데이터가 쌓여서 fetch 요청이 처리된 경우 


## 3. 참고자료
- https://medium.com/@kevin.michael.horan/distributed-video-streaming-with-python-and-kafka-551de69fe1dd


## 4. Sending Video example 
- video 
https://www.programcreek.com/python/example/98438/kafka.KafkaProducer
```python
def main(n):
    """Stream the video into a Kafka producer in an infinite loop"""
    
    topic = choose_channel(n)
    video_reader = imageio.get_reader(DATA + topic + '.mp4', 'ffmpeg')
    metadata = video_reader.get_meta_data()
    fps = metadata['fps']

    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             batch_size=15728640,
                             linger_ms=1000,
                             max_request_size=15728640,
                             value_serializer=lambda v: json.dumps(v.tolist()))
    
    while True:
        video_loop(video_reader, producer, topic, fps) 
```

```
        self.producer = KafkaProducer(bootstrap_servers=str(self.hostIP)+":"+str(self.hostPort), api_version=(0,10),
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                      compression_type='gzip') 
```

## 9. 인증관련
```
sudo keytool -import -alias shibbolethnet -keystore /Library/Java/JavaVirtualMachines/jdk-11.0.7.jdk/Contents/Home/lib/security/cacerts -file ~/Downloads/SK_SSL


curl -X GET https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.der -o lets-encrypt-x3-cross-signed.der; 


sudo keytool -trustcacerts -keystore /Library/Java/JavaVirtualMachines/jdk-11.0.7.jdk/Contents/Home/lib/security/cacerts -storepass changeit -noprompt -importcert -alias lets-encrypt-x3-cross-signed -file lets-encrypt-x3-cross-signed.der
```
