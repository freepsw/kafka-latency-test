package kafka;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRebalanceListener;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.config.SslConfigs;
import org.apache.kafka.clients.producer.Callback;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Collection;
import java.util.Collections;
import java.util.Properties;
import java.util.Random;
import java.awt.image.BufferedImage;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.FileSystems;
import java.io.IOException;
import javax.imageio.ImageIO;
import java.io.ByteArrayOutputStream;

public class ProducerConsumer {

    public static void main(String[] args) {
        //run the program with args: producer/consumer broker:port

        String img_file="";
        String groupId = "my-group", brokers = "freepsw-template-centos-4cpu-1:9092", topic = "test", type = "producer";
        if (args.length == 2) {
            type = args[0];
            brokers = args[1];

        } else {
            type = "producer";
            brokers = "freepsw-template-centos-4cpu-1:9092";
        }
        img_file = "/Users/skiper/work/DevTools/github/TestPy/data/"+ args[2];
        System.out.println(img_file);

        Properties props = new Properties();

        //configure the following three settings for SSL Encryption
//        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SSL");
//        props.put(SslConfigs.SSL_KEYSTORE_LOCATION_CONFIG, "/etc/pki/tls/keystore.jks");
//        props.put(SslConfigs.SSL_KEYSTORE_PASSWORD_CONFIG, "password");
//        props.put(SslConfigs.SSL_KEY_PASSWORD_CONFIG, "password");


        if (type.equals("consumer")) {
            props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, brokers);
            props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
            props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
            props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
            props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
            KafkaConsumer < byte[], byte[] > consumer = new KafkaConsumer < > (props);
            TestConsumerRebalanceListener rebalanceListener = new TestConsumerRebalanceListener();
            consumer.subscribe(Collections.singletonList(topic), rebalanceListener);
            final int giveUp = 100;
            int noRecordsCount = 0;
            while (true) {
                final ConsumerRecords < byte[], byte[] > consumerRecords =
                    consumer.poll(1000);

                if (consumerRecords.count() == 0) {
                    noRecordsCount++;
                    if (noRecordsCount > giveUp) break;
                    else continue;
                }

                consumerRecords.forEach(record -> {
                    System.out.printf("Consumer Record:(%d, %s, %d, %d)\n",
                        record.key(), record.value(),
                        record.partition(), record.offset());
                });

                consumer.commitAsync();
            }
            consumer.close();
            System.out.println("DONE");

        } else {
            File file = new File(img_file);
            BufferedImage image = null;
            byte[] encodedImage = null;
            byte[] fileData = null;
            try
            {
                image = ImageIO.read(file);
                ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
                ImageIO.write(image, "png", outputStream);
                encodedImage = outputStream.toByteArray();
//                ImageIO.write(image, "jpg", new File("I:/output.jpg"));
                //http://www.idata.co.il/2016/09/moving-binary-data-with-kafka/
                fileData=Files.readAllBytes(FileSystems.getDefault().getPath("/Users/skiper/work/DevTools/github/TestPy/data/3m.jpg"));
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }



            System.out.println("done");

            props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, brokers);
            props.put(ProducerConfig.ACKS_CONFIG, "all");
            props.put(ProducerConfig.RETRIES_CONFIG, 0);
            props.put(ProducerConfig.MAX_REQUEST_SIZE_CONFIG, 50000000);
            props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
//            props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
//            props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.ByteArraySerializer");
            props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.ByteArraySerializer");


            KafkaProducer < String, byte[] > producer = new KafkaProducer < > (props);
            TestCallback callback = new TestCallback();
            Random rnd = new Random();
            // So we can generate random sentences
            Random random = new Random();
            String[] sentences = new String[] {
                "Python is a language, not a reptile"
            };
            for (int i = 0; i < 1; i++) {
                // Pick a sentence at random
                String sentence = sentences[random.nextInt(sentences.length)];
                // Send the sentence to the test topic
//                ProducerRecord < String, String > data = new ProducerRecord < String, String > (topic, sentence);
                ProducerRecord < String, byte[] > data = new ProducerRecord < String, byte[] > (topic, encodedImage);
                long startTime = System.currentTimeMillis();
                producer.send(data, callback);
                long elapsedTime = System.currentTimeMillis() - startTime;
                System.out.println("Sent this sentence: " + sentence + " in " + elapsedTime + " ms");

            }
            System.out.println("Done");
            producer.flush();
            producer.close();
        }

    }

    private static class TestConsumerRebalanceListener implements ConsumerRebalanceListener {
        @Override
        public void onPartitionsRevoked(Collection < TopicPartition > partitions) {
            System.out.println("Called onPartitionsRevoked with partitions:" + partitions);
        }

        @Override
        public void onPartitionsAssigned(Collection < TopicPartition > partitions) {
            System.out.println("Called onPartitionsAssigned with partitions:" + partitions);
        }
    }

    private static class TestCallback implements Callback {
        @Override
        public void onCompletion(RecordMetadata recordMetadata, Exception e) {
            if (e != null) {
                System.out.println("Error while producing message to topic :" + recordMetadata);
                e.printStackTrace();
            } else {
                String message = String.format("sent message to topic:%s partition:%s  offset:%s", recordMetadata.topic(), recordMetadata.partition(), recordMetadata.offset());
                System.out.println(message);
            }
        }
    }

}
