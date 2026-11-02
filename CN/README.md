# Computer Networks (CN) Laboratory Experiments

This directory contains standalone, standard C implementations for core Data Link & Transport layer error detection and correction algorithms.

## Experiments Included:

### 1. Experiment 6: CRC (Cyclic Redundancy Check)
- **File:** `crc.c`
- **Description:** Implements Modulo-2 binary division using generator polynomials to compute remainder codewords and verify frame integrity at the receiver.
- **Compilation & Execution:**
  ```bash
  gcc crc.c -o crc
  ./crc
  ```

### 2. Experiment 7: Hamming Code Error Detection & Correction
- **File:** `hamming.c`
- **Description:** Generates parity bits at power-of-two positions ($2^i$), computes error syndrome at receiver, identifies the corrupted bit position, and performs single-bit correction.
- **Compilation & Execution:**
  ```bash
  gcc hamming.c -o hamming
  ./hamming
  ```

### 3. Experiment 8: Checksum Error Detection
- **File:** `checksum.c`
- **Description:** Implements 8-bit one's complement addition with end-around carry and complement checksum generation matching Internet TCP/IP checksum principles.
- **Compilation & Execution:**
  ```bash
  gcc checksum.c -o checksum
  ./checksum
  ```

---
*Generated via LabX Remote Platform*

