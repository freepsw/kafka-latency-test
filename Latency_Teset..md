# Sending large image files to apache kafka (with low latency) 
- Test code and scripts for image transmission using apache kafka  
- 최근 vision model(cnn, resnet 등)이 많이 서비스되면서, 
- 사이즈가 큰 영상(이미지)를 효율적으로 모델에 전송하기 위한 기술로 apache kafka를 활용하고 있다.
    - AWS는 이미 Kineiss video stream을 통해서 영상을 스트리밍하는 서비스를 제공하고 있다. 
- 그래서 Kafka에서 이미지를 전송하는 간단한 테스트를 진행하였고,
- 이 과정에서 latency를 얼마나 줄여주는지를 확인해 보았다.(HTTP 프로토콜과 비교하여)
- [현재 까지 결론]
    - Apache Kafka는 대량의 요청 처리를 위한 throughtput에 최적화 된 솔루션임.
    - 처음 consumer가 broker로부터 partition을 할당 받는 시간 소요 (1~2초, 해당 설정 확인 필요)
    - 이후 kafka으 latency는 REST API(HTTP)와 비교하여 더 빠른 성능을 제공함. 

## STEP 0. Test Environments
### Server Spec
- GCP Instance(us-central1-a) : CentOS 7
- 8 cpus, 32G Memory 

### Software Spec 
- Apache Kafka (2.12-2.5.0)
- Python Library : kafka-python(v2.0.2), confluent-kafka(v1.4.0)
- Scala Library : kakfka client lib (org.apache.kafka.clients.*)

### Test Data (images)
- 1mb.jpg  : base64 변환 (1,458,612 byte)
- 3mb.jpg  : base64 변환 (4,448,128 byte)
- 5mb.jpg  : base64 변환 (6,249,084 byte)
- 10mb.jpg : base64 변환 (13,566,276 byte)

## STEP 1. Test Scenario 
- Latency를 비교하기 위해서 REST API와 다양한 kafka library를 활용함. 
- 그림 추가 ()
- Scenario 1. REST API latency 측정 
- Scenario 2. kafka-python library latency 측정 
- Scenario 3. confluent-kafka library latency 측정 
- Scenario 4. Kafka EndtoEndLatency Class 실행 및 측정 


## STEP 2. Run Test 
### Scenario 1. REST API latency 측정 
- 전달하는 데이터 사이즈는 동일하며, 
- web client(producer)에서 web server(consumer)로 전달되는 시간을 비교한다. 

#### Latency 측정 결과
- 1mb.jpg  : 0.0146 ms
- 3mb.jpg  : 0.0170 ms
- 5mb.jpg  : 0.0263 ms
- 10mb.jpg : 0.0553 ms
 


### Scenario 2. kafka-python library latency 측정 
- 직접 producer/consumer를 구현하여, 
- producer에서 send()를 시작한 시간에서
- consumer에서 데이터를 모두 수신 완료한 시간을 측정한다. 

### Scenario 3. confluent-kafka library latency 측정 
- 직접 producer/consumer를 구현하여, 
- producer에서 send()를 시작한 시간에서
- consumer에서 데이터를 모두 수신 완료한 시간을 측정한다. 

### Scenario 4. Kafka EndtoEndLatency Class 실행 및 측정 
- Apache Kafka에서 기본으로 제공하는 Class를 활용하여 테스트 및 latency 측정
- https://github.com/apache/kafka/blob/trunk/core/src/main/scala/kafka/tools/EndToEndLatency.scala


### STEP 2. Run Test (EndToEndLatency)

### 

```
1458612
4448128
6249084
13566276
bin/kafka-run-class.sh kafka.tools.EndToEndLatency kafka-test:9092 test8 5 1 13566276 config/producer.properties

bin/kafka-run-class.sh kafka.tools.EndToEndLatency skcc11n00142:9092 test8 5 1 13566276 config/producer.properties

```











## STEP 1. Kafka Configuration 


### Production Server configuration example 
- 실제 운영환경에서 Kafka에서 고려할 설정들
- https://kafka.apache.org/08/documentation.html
#### Broker Configuration 
- disk flush rate 
    - 처리량 관점에서는 너무 잦을 수록 성능이 낮아짐 (disk에 쓰는 속도)
    - latency 관점에서는 빨리 자주 써야 응답이 빨라짐 

    
#### Producer Configration 
- compresssion
- sysnc vs asyc send
- batch size (for async producer ???)

#### Consumer Configuration 
- fetch size 




#### Examples (실제 운영환경에서 권장)
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


#### Apache Kafka, Purgatory, and Hierarchical Timing Wheels
https://www.confluent.io/blog/apache-kafka-purgatory-hierarchical-timing-wheels/



## STEP 2. Run apache kafka (jmx enabled)

### Run Broker 
```
> wget http://apache.tt.co.kr/kafka/2.5.0/kafka_2.12-2.5.0.tgz
> tar -xzf kafka_2.12-2.5.0.tgz
> cd kafka_2.12-2.5.0

> bin/zookeeper-server-start.sh config/zookeeper.properties

> env JMX_PORT=9999 bin/kafka-server-start.sh config/server.properties
```

### Create topic (resize message size per topic)
- http://kafka.apache.org/documentation/#topicconfigs

```
> bin/kafka-topics.sh --bootstrap-server freepsw-template-centos-4cpu-1:9092 --create --topic test2 --partitions 1 \
  --replication-factor 1 --config max.message.bytes=15000000 --config flush.messages=1

# or  
> bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name test \
    --alter --add-config max.message.bytes=15000000

```

### Describe topic (resize message size per topic)
- https://gist.github.com/ursuad/e5b8542024a15e4db601f34906b30bb5
```
> bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic test2
Topic: test2	PartitionCount: 1	ReplicationFactor: 1	Configs: max.message.bytes=15000000,flush.messages=1
	Topic: test2	Partition: 0	Leader: 0	Replicas: 0	Isr: 0

> bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list freepsw-template-centos-4cpu-1:9092 --topic test2 --time -1 --offsets 1 | awk -F ":" '{sum += $3} END {print sum}'

bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list freepsw-template-centos-4cpu-1:9092 --topic test2
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test2

# Check Lag 
bin/kafka-consumer-groups.sh  --describe  --group my-group  --bootstrap-server freepsw-template-centos-4cpu-1:9092 
bin/kafka-consumer-groups.sh  --describe  --group my-group  --bootstrap-server skcc11n00142:9092 
```



## STEP 3. Something wrong (Too high latency)
- 동일한 데이터를 rest api(post)로 보낸것과 비교하면, 1초 이상 느리게 전송됨. 
    - Producer Send Time - Consumer Receive Time
- 특이한 부분은 데이터의 사이즈에 상관없이 약 1.4초 정도의 Delay가 발생한다. 
- 테스트 데이터 및 
    - 10byte
    - 1.4mb 
    - 4.4mb
    - 6.1mb

### Latency Test 
- GCP Instance(4cpu, 16G)를 사용했고, 
- 동일한 Node에서 Procuder/Consumer, Web-Client/Web-Server를 구성하여 테스트함.

#### REST API
- Test Size : 6mb (json)
- Latency(Processing) : 
