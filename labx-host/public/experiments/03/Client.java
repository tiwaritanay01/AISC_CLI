import java.io.*;
import java.net.*;

public class Client {
    public static final String HOST = "127.0.0.1";
    public static final int PORT = 5000;

    public static void main(String[] args) {
        System.out.println("[Client] Connecting to " + HOST + ":" + PORT + "...");
        try (Socket socket = new Socket(HOST, PORT);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            System.out.println("[Client] Connected successfully!");
            String payload = "Hello from LabX Java Client!";
            System.out.println("[Client] Sending: " + payload);
            out.println(payload);

            String reply = in.readLine();
            System.out.println("[Client] Reply from server: " + reply);

        } catch (IOException e) {
            System.err.println("[Client] Connection error: " + e.getMessage());
        }
    }
}
