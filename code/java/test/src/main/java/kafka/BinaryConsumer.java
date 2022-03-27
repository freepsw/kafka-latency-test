package kafka;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

/**
 *
 * @author guys
 */
public class BinaryConsumer {
    Properties props;
    KafkaConsumer<String, byte[]> consumer;
    String outDir;

    /**
     *
     */

    public BinaryConsumer() throws IOException
    {
// setting Kafka configuration
        props = new Properties();
        props.put("bootstrap.servers", "freepsw-template-centos-4cpu-1:9092");
        props.put("group.id", "my-group");
        props.put("enable.auto.commit", "true");
//        props.put("compression.type","snappy");
        props.put("fetch.message.max.bytes","50000000");
        props.put("auto.commit.interval.ms", "1000");
        props.put("session.timeout.ms", "30000");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.ByteArrayDeserializer");
        outDir="./data";

    }

    public void createConsumer()
    {
        consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList("test"));
    }

    public void start() throws IOException
    {
        System.out.println("test");
        String name="resultfile";
        ByteArrayOutputStream bos=new ByteArrayOutputStream();
//Loop endlessly and poll for new kafka records.
        while (true) {
            ConsumerRecords<String, byte[]> records = consumer.poll(100);
            for (ConsumerRecord<String, byte[]> record : records)
            {
// Test weather we have reached EOF
                if (record.value()==null)
                {
// we reached EOF, write it to disk.
                    System.out.println("Writing file "+name);
                    writeFile(name,bos.toByteArray());
                    bos.reset();
                }
                else
                {
// this is just another chunk, accumulate it in memory
                    name=record.key();
                    bos.write(record.value());
                }
            }
        }
    }


    private void writeFile(String name,byte[] rawdata) throws IOException
    {
//
//        File f=new File(outDir);
//        if (!f.exists())
//            f.mkdirs();

        FileOutputStream fos=new FileOutputStream("/Users/skiper/work/DevTools/github/TestPy/data/out.dat");
        fos.write(rawdata);
        fos.flush();
        fos.close();


    }


    public static void main(String[] args) {
        try {
            BinaryConsumer abc;
            abc=new BinaryConsumer();
            abc.createConsumer();
            abc.start();
        } catch (IOException ex) {
            Logger.getLogger(BinaryConsumer.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

}