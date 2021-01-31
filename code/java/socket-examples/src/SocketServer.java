import java.net.*;
import java.io.*;
public class SocketServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = null;
        try {
            serverSocket = new ServerSocket(8888);
            InputStream in = null;
            OutputStream out = null;
            while(true){
                try {
                    Socket socket = serverSocket.accept();
                    System.out.println("Received a request");
                    long start = System.currentTimeMillis();

                    String fileName = "image-" + System.currentTimeMillis() + ".jpg";
                    BufferedInputStream bis = new BufferedInputStream(socket.getInputStream());
//                    File f = new File(fileName);
//                    BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(f));
                    int bytesWritten = 0;
                    int b;
                    while ((b = bis.read()) != -1) {
//                        bos.write(b);
                        bytesWritten++;
                    }
//                    bos.close();
                    bis.close();

                    long end = System.currentTimeMillis();
                    float time_elasped = end - start;
                    System.out.println("\r\nReceived Time: " + time_elasped/1000);
                    socket.close();

                } catch (IOException ex) {
                    System.out.println("Can't accept client connection. ");
                }
            }
        }
        catch (IOException ex) {
            System.out.println("Can't setup server on this port number.");
        }
    }
}
