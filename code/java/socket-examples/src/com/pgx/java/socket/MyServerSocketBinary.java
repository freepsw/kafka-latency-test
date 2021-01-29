package com.pgx.java.socket;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
public class MyServerSocketBinary {
    private ServerSocket server;
    public MyServerSocketBinary(String ipAddress) throws Exception {
        if (ipAddress != null && !ipAddress.isEmpty())
            this.server = new ServerSocket(8888, 1, InetAddress.getByName(ipAddress));
        else
            this.server = new ServerSocket(0, 1, InetAddress.getLocalHost());
    }
    private void listen() throws Exception {

        // Accept new client connection
        //
        String data = null;
        Socket client = this.server.accept();
        String clientAddress = client.getInetAddress().getHostAddress();
        System.out.println("\r\nNew connection from " + clientAddress);
        //
        // Read binary data from client socket and write to file
        //
        long start = System.currentTimeMillis();

////      Option 1 read line from client
//        BufferedReader bis = new BufferedReader(
//                new InputStreamReader(client.getInputStream()));
//        while ( (data = bis.readLine()) != null ) {
//            System.out.println("\r\nMessage from " + clientAddress + ": " + data);
//        }

//      Option 2 Save data to file
        BufferedInputStream bis = new BufferedInputStream(client.getInputStream());

        String fileName = "image-" + System.currentTimeMillis() + ".jpg";
        MyFileWriter fw = new MyFileWriter();
        long end = System.currentTimeMillis();
        float time_elasped = end - start;
        System.out.println("\r\nReceived Time: " + time_elasped);
//        int fileSize = fw.writeFile(fileName, bis);
//        System.out.println("\r\nWrote " + fileSize + " bytes to file " + fileName);
//        bis.close();
//
//        long finish = System.currentTimeMillis();
//        long timeElapsed = finish - start;
//        System.out.println("\r\nElapsed Time: " + timeElapsed/1000);

        // Close socket connection
        //
//        client.close();


    }
    public InetAddress getSocketAddress() {
        return this.server.getInetAddress();
    }
    public int getPort() {
        return this.server.getLocalPort();
    }
    public static void main(String[] args) throws Exception {
        MyServerSocketBinary app = new MyServerSocketBinary("localhost");

        System.out.println("\r\nRunning Server (Image): " +
                "Host=" + app.getSocketAddress().getHostAddress() +
                " Port=" + app.getPort());

        app.listen();
    }
}