/*
 * Computer Networks Laboratory - Socket Programming
 * Experiment: Implementation of TCP Socket Client in Java
 */

import java.io.*;
import java.net.*;

public class TCPClient {
    private static final String SERVER_HOST = "127.0.0.1";
    private static final int SERVER_PORT = 5000;

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println("           TCP Client Initializing                ");
        System.out.println("==================================================");
        System.out.println("[*] Connecting to server at " + SERVER_HOST + ":" + SERVER_PORT + "...");

        try (
            Socket socket = new Socket(SERVER_HOST, SERVER_PORT);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader console = new BufferedReader(new InputStreamReader(System.in))
        ) {
            System.out.println("[+] Successfully connected to server!");

            // Read welcome greeting
            String greeting = in.readLine();
            System.out.println("[Server]: " + greeting);

            // Pre-defined test messages if console is non-interactive, or interactive loop
            String[] testMessages = {"Hello Server!", "Testing Computer Networks Socket", "Socket Programming in Java", "exit"};
            int msgIdx = 0;

            while (true) {
                System.out.print("\nEnter message to send (or 'exit' to quit): ");
                String userInput = null;
                if (System.console() != null) {
                    userInput = console.readLine();
                } else if (msgIdx < testMessages.length) {
                    userInput = testMessages[msgIdx++];
                    System.out.println(userInput);
                }

                if (userInput == null || userInput.trim().isEmpty()) {
                    continue;
                }

                // Send message to server
                out.println(userInput);

                // Receive response
                String response = in.readLine();
                if (response != null) {
                    System.out.println("[Response]: " + response);
                }

                if (userInput.equalsIgnoreCase("exit") || userInput.equalsIgnoreCase("quit")) {
                    System.out.println("[*] Disconnecting from server...");
                    break;
                }
            }
        } catch (ConnectException e) {
            System.err.println("[!] Connection failed: Is the server running on " + SERVER_HOST + ":" + SERVER_PORT + "?");
        } catch (IOException e) {
            System.err.println("[!] I/O Exception: " + e.getMessage());
        }
    }
}

/*
============================================================================
HOW TO RUN THIS EXPERIMENT:
============================================================================
Prerequisites: JDK 8 or higher (`javac -version` and `java -version`).

1. Terminal 1 (Start Server First):
   javac TCPServer.java
   java TCPServer

2. Terminal 2 (Start Client):
   javac TCPClient.java
   java TCPClient

3. Communication & Exit:
   Enter any text message to transmit to the server and receive the echo.
   Type 'exit' to terminate the client connection cleanly.
============================================================================
EXPERIMENT THEORY (Computer Networks - Java Socket Programming Client):
============================================================================
The client application acts as the initiator in the client-server architecture.
In Java, constructing a Socket(host, port) performs the DNS resolution and
TCP handshake with the remote listening host.

Key Operational Steps:
1. Address Resolution: Locates target host by domain name or IPv4/IPv6 loopback.
2. Connection Request: Sends SYN packet to server's designated port.
3. Stream Binding: Upon receiving SYN-ACK and completing handshake, local port
   is dynamically assigned by the OS, and I/O streams are attached.
4. Transmission & Reception: Writes data to OutputStream, reads responses from
   InputStream.
5. Graceful Disconnection: Sends FIN packet when closing the socket, ensuring
   all buffered packets are acknowledged.
============================================================================
*/

