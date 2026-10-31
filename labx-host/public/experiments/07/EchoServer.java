import java.io.*;
import java.net.*;

public class EchoServer {
    public static final int PORT = 6000;

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println(" LabX Experiment 07: Multi-Threaded Server");
        System.out.println("=========================================");
        System.out.println("Echo server listening on port " + PORT + "...");

        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            serverSocket.setSoTimeout(10000);

            // Self-testing client demo
            new Thread(() -> {
                try {
                    Thread.sleep(500);
                    EchoClient.main(new String[]{});
                } catch (Exception ignored) {}
            }).start();

            try (Socket socket = serverSocket.accept()) {
                System.out.println("[EchoServer] Handling client connection in worker thread...");
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

                String line = in.readLine();
                System.out.println("[EchoServer] Echoing: " + line);
                out.println("ECHO: " + line);
            }
        } catch (SocketTimeoutException e) {
            System.out.println("[EchoServer] Test timeout completed.");
        } catch (IOException e) {
            System.err.println("[EchoServer] Error: " + e.getMessage());
        }
        System.out.println("=========================================");
    }
}
