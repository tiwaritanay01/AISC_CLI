import java.io.*;
import java.net.*;

public class EchoClient {
    public static void main(String[] args) {
        try (Socket s = new Socket("127.0.0.1", 6000);
             PrintWriter out = new PrintWriter(s.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()))) {

            String msg = "Testing Concurrent Connection";
            out.println(msg);
            System.out.println("[EchoClient] Sent: " + msg);
            System.out.println("[EchoClient] Received: " + in.readLine());
        } catch (Exception e) {
            System.err.println("[EchoClient] Failed: " + e.getMessage());
        }
    }
}
