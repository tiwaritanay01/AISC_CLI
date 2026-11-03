# Computer Networks (CN) Laboratory Experiments

This directory contains standalone, standard implementations for core Data Link, Transport, and Application layer protocols and error detection algorithms.

## Experiments Included:

### 1. Experiment 6: CRC (Cyclic Redundancy Check)
- **File:** `crc.c`
- **Language:** C
- **Description:** Implements Modulo-2 binary division using generator polynomials to compute remainder codewords and verify frame integrity at the receiver.
- **Compilation & Execution:**
  ```bash
  gcc crc.c -o crc
  ./crc
  ```

### 2. Experiment 7: Hamming Code Error Detection & Correction
- **File:** `hamming.c`
- **Language:** C
- **Description:** Generates parity bits at power-of-two positions ($2^i$), computes error syndrome at receiver, identifies the corrupted bit position, and performs single-bit correction.
- **Compilation & Execution:**
  ```bash
  gcc hamming.c -o hamming
  ./hamming
  ```

### 3. Experiment 8: Checksum Error Detection
- **File:** `checksum.c`
- **Language:** C
- **Description:** Implements 8-bit one's complement addition with end-around carry and complement checksum generation matching Internet TCP/IP checksum principles.
- **Compilation & Execution:**
  ```bash
  gcc checksum.c -o checksum
  ./checksum
  ```

### 4. Experiment 9: Client-Server Socket Programming
- **Files:** `TCPServer.java`, `TCPClient.java`
- **Language:** Java
- **Description:** Two-way stream-based client-server communication using Java `ServerSocket` and `Socket` APIs over TCP port 5000 with request-response echoing and session termination.
- **Compilation & Execution:**
  ```bash
  # In terminal 1:
  javac TCPServer.java
  java TCPServer

  # In terminal 2:
  javac TCPClient.java
  java TCPClient
  ```

### 5. Experiment 10: Dijkstra's Shortest Path Routing Algorithm
- **File:** `dijkstra.c`
- **Language:** C
- **Description:** Implements Link State Routing (OSPF) to compute the single-source shortest path tree and generate complete routing tables with optimal costs and intermediate node paths.
- **Compilation & Execution:**
  ```bash
  gcc dijkstra.c -o dijkstra
  ./dijkstra
  ```

---
*Generated via LabX Remote Platform*

SE prompt : I have added chapter 2.pdf in this directory now using that make UML diagrams make a seperate subjetc named SE and add use case and activity diagrams , data flow diagram mermaid.js code for these list of case studies C:\dev\CLI_AISC\CASE STUDIES.pdf 
these 3 keep the colors black and white not colorful follow all stnadard drawing convenrtions and then how will you give it to me for this particular topic say hospital/usecase in this types of commands to paste the mermaid.js code
this is the diagram list whose code is needed Class 
Use 
Data flow
Activity or state
