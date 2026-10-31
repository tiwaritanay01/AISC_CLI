import java.io.*;
import java.net.*;

public class Server {
    public static final int PORT = 5000;

    public static void main(String[] args) {
        System.out.println("=========================================");
        System.out.println(" LabX Experiment 03: Java Socket Server");
        System.out.println("=========================================");
        System.out.println("Server listening on port " + PORT + "...");

        // Auto-run simulation or accept single client
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            // Set 15-second timeout for unattended test runs
            serverSocket.setSoTimeout(15000);
            
            // Start client in background thread for self-testing demo
            new Thread(() -> {
                try {
                    Thread.sleep(500);
                    Client.main(new String[]{});
                } catch (Exception e) {
                    // Ignore background demo client errors
                }
            }).start();

            try (Socket socket = serverSocket.accept();
                 BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                 PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

                System.out.println("[Server] Connection accepted from: " + socket.getRemoteSocketAddress());
                String message = in.readLine();
                System.out.println("[Server] Received from client: " + message);

                String response = "Server ACK: Received message [" + message + "]";
                out.println(response);
                System.out.println("[Server] Sent response to client: " + response);
            }
        } catch (SocketTimeoutException e) {
            System.out.println("[Server] Timeout reached waiting for client.");
        } catch (IOException e) {
            System.err.println("[Server] I/O Exception: " + e.getMessage());
        }
        System.out.println("=========================================");
    }
}
