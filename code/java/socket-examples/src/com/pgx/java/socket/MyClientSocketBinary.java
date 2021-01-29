package com.pgx.java.socket;
import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
public class MyClientSocketBinary {
    private Socket socket;
    private MyFileReader fileReader;
    private MyClientSocketBinary(InetAddress serverAddress, int serverPort) throws Exception {
        this.socket = new Socket(serverAddress, serverPort);
    }

    private void sendFile(String fileName) throws IOException {
        //
        // Read file from disk
        //
        fileReader = new MyFileReader();
        byte[] data = fileReader.readFile(fileName);
        //
        // Send binary data over the TCP/IP socket connection
        //
        for (byte i : data) {
            this.socket.getOutputStream().write(i);
        }

        System.out.println("\r\nSent " + data.length + " bytes to server.");
    }
    /**
     * Requires 3 arguments:
     *     1: TCP/IP server host name or IP address
     *     2: TCP/IP server port number
     *     3: Absolute path and file name of file to send
     *
     * @param args
     * @throws Exception
     */
    public static void main(String[] args) throws Exception {
        MyClientSocketBinary client = new MyClientSocketBinary(
                InetAddress.getByName("localhost"),
                8888);

        System.out.println("\r\nConnected to Server: " + client.socket.getInetAddress());
        long start = System.currentTimeMillis();
//        client.sendFile("/Users/skiper/work/DevTools/github/kafka-latency-test/code/python/data/1mb.jpg");

        File file = new File("/Users/skiper/work/DevTools/github/kafka-latency-test/code/python/data/1mb.jpg");

        byte[] bytes = new byte[16 * 1024];
        InputStream in = new FileInputStream(file);
        OutputStream out = client.socket.getOutputStream();

        int count;
        while ((count = in.read(bytes)) > 0) {
            out.write(bytes, 0, count);
        }

        out.close();
        in.close();
        client.socket.close();



        long finish = System.currentTimeMillis();
        float timeElapsed = (finish - start);
        float totalTime = timeElapsed/1000;

        System.out.println("\r\nElapsed Time: " + totalTime);
    }
}