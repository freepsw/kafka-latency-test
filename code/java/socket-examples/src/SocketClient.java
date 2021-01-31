import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;

public class SocketClient {
    public static void main(String[] args) throws Exception {
        File file = new File("./1mb.jpg");

        for(int i =0; i <10; i++) {
            long start = System.currentTimeMillis();
            Socket socket = new Socket(InetAddress.getByName("localhost"), 8888);
            System.out.println("\r\nConnected to Server: " + socket.getInetAddress());
            byte[] bytes = new byte[16 * 1024];
            InputStream in = new FileInputStream(file);
            OutputStream out = socket.getOutputStream();
            int count;
            while ((count = in.read(bytes)) > 0) {
//                out.write(bytes, 0, count);
            }
//            out.close();
            in.close();
            socket.close();

            long finish = System.currentTimeMillis();
            float timeElapsed = (finish - start);
            System.out.println("\r\nElapsed Time: " + timeElapsed/1000);
        }
    }
}
