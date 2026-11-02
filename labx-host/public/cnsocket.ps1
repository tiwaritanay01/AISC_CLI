# LabX Remote: CN Exp 09 (Experiment 9 – Client-Server Socket Programming in Java)
$filename = "TCPServer.java"
$code = @'
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

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White

$filename = "TCPClient.java"
$code = @'
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

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White
