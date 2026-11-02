/*
 * Computer Networks Laboratory - Socket Programming
 * Experiment: Implementation of Concurrent / Two-Way TCP Socket Server in Java
 */

import java.io.*;
import java.net.*;

public class TCPServer {
    private static final int PORT = 5000;

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println("   TCP Echo & Communication Server Started        ");
        System.out.println("==================================================");
        System.out.println("[*] Server listening on port: " + PORT);

        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("[*] Waiting for incoming client connection...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                String clientIP = clientSocket.getInetAddress().getHostAddress();
                int clientPort = clientSocket.getPort();
                System.out.println("\n[+] Client connected from: " + clientIP + ":" + clientPort);

                // Handle client in session
                handleClient(clientSocket);
                break; // Session completed
            }
        } catch (IOException e) {
            System.err.println("[!] Server Exception: " + e.getMessage());
        }
    }

    private static void handleClient(Socket socket) {
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader console = new BufferedReader(new InputStreamReader(System.in))
        ) {
            out.println("CONNECTED: Welcome to Java TCP Server. Type 'exit' to quit.");

            String clientMsg;
            while ((clientMsg = in.readLine()) != null) {
                System.out.println("[Client]: " + clientMsg);
                if (clientMsg.equalsIgnoreCase("exit") || clientMsg.equalsIgnoreCase("quit")) {
                    out.println("BYE: Connection closed by request.");
                    System.out.println("[-] Client requested termination.");
                    break;
                }

                String echoResponse = "SERVER ECHO: " + clientMsg.toUpperCase();
                out.println(echoResponse);
            }
        } catch (IOException e) {
            System.err.println("[!] Communication error: " + e.getMessage());
        } finally {
            try {
                socket.close();
                System.out.println("[*] Client socket closed successfully.");
            } catch (IOException ex) {
                System.err.println("[!] Error closing socket: " + ex.getMessage());
            }
        }
    }
}

/*
============================================================================
EXPERIMENT THEORY (Computer Networks - Java Socket Programming Server):
============================================================================
A Network Socket is one endpoint of a two-way communication link between
two programs running over a computer network. In Java, networking APIs are
encapsulated in the java.net package, built on top of the TCP/IP stack.

Core Concepts:
1. TCP (Transmission Control Protocol):
   A connection-oriented, reliable, byte-stream transport layer protocol.
   Before data transfer begins, a three-way handshake (SYN, SYN-ACK, ACK)
   establishes a virtual circuit between client and server.

2. ServerSocket (Server Endpoint):
   The ServerSocket class binds to a specific port on the local machine and
   listens for incoming connection requests via its blocking accept() method.
   When a connection is received, accept() returns a dedicated Socket instance
   for communicating with that specific client.

3. Socket (Client Endpoint):
   The Socket class initiates the TCP connection by specifying the server's
   IP address (or hostname) and port number.

4. Stream-Based I/O:
   - InputStream / BufferedReader: Reads incoming byte/character streams from the
     remote endpoint.
   - OutputStream / PrintWriter: Transmits outgoing byte/character streams to the
     remote endpoint with automatic flushing.

5. Connection Lifecycle:
   1) Server creates ServerSocket(port) and invokes accept().
   2) Client constructs Socket(host, port) to establish handshake.
   3) Both sides exchange data through input/output streams.
   4) Connections are cleanly terminated by closing stream handles and sockets.
============================================================================
*/
