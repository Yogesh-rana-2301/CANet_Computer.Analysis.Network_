#   Transport Layer — Basics

> The Transport Layer sits between the Application Layer and the Network Layer. It is responsible for delivering data between **specific processes** (not just hosts) and can optionally provide reliability.

---

## 1. Functions of the Transport Layer

```
┌──────────────────────────────────────────────────────────────────┐
│                     Transport Layer Functions                    │
│                                                                  │
│  1. Process-to-Process Delivery   (Ports)                        │
│  2. Multiplexing & Demultiplexing (Many apps, one network)       │
│  3. Segmentation & Reassembly     (Break data, put back)         │
│  4. Connection Management         (TCP: establish/terminate)     │
│  5. Reliable Delivery             (TCP: ACKs + retransmission)   │
│  6. Flow Control                  (TCP: don't overwhelm receiver)│
│  7. Congestion Control            (TCP: don't overwhelm network) │
│  8. Error Detection               (Checksum in header)           │
└──────────────────────────────────────────────────────────────────┘
```

| Function | TCP | UDP |
|---------|-----|-----|
| Process-to-process delivery | ✅ | ✅ |
| Multiplexing/Demultiplexing | ✅ | ✅ |
| Segmentation & Reassembly | ✅ | ✅ (application must handle) |
| Connection management | ✅ (3-way handshake) | ❌ |
| Reliability (ACK + retransmit) | ✅ | ❌ |
| Flow control | ✅ (rwnd) | ❌ |
| Congestion control | ✅ (CWND) | ❌ |
| Error detection | ✅ (checksum) | ✅ (checksum, optional) |

---

## 2. Process-to-Process Delivery

### 2.1 The Problem

The **Network Layer (IP)** delivers packets to a **host** (identified by IP address). But a host may be running dozens of applications simultaneously — how does the OS know which application should receive an incoming packet?

```
Your laptop receives a packet destined for IP 192.168.1.10
  But which process gets it?
    • Chrome browser (HTTP)?
    • Spotify streaming?
    • Slack messaging?
    • SSH client?

The IP address gets it to the right machine.
The PORT NUMBER gets it to the right process.
```

### 2.2 Port Numbers

A **port number** is a 16-bit integer (0–65535) that identifies a specific process or service on a host.

```
Transport Layer Endpoint = IP Address + Port Number = SOCKET

Source socket:      192.168.1.10 : 54321   (your browser tab)
Destination socket: 142.250.68.46 : 443    (Google HTTPS)
```

### 2.3 Port Number Ranges

| Range | Name | Description |
|-------|------|-------------|
| **0–1023** | Well-known / System ports | Reserved for standard services (requires root/admin) |
| **1024–49151** | Registered ports | Registered by IANA for specific applications |
| **49152–65535** | Ephemeral / Dynamic ports | Assigned temporarily by OS for client connections |

**Well-Known Port Examples:**
| Port | Protocol | Service |
|------|---------|---------|
| 20 | TCP | FTP Data |
| 21 | TCP | FTP Control |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | UDP/TCP | DNS |
| 67/68 | UDP | DHCP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 443 | TCP | HTTPS |
| 3306 | TCP | MySQL |
| 5432 | TCP | PostgreSQL |
| 6379 | TCP | Redis |
| 8080 | TCP | HTTP Alternate |

---

## 3. Multiplexing and Demultiplexing

### 3.1 Multiplexing (Sender Side)

The transport layer **collects data** from multiple application processes, adds transport headers (including port numbers), and sends them down to the network layer.

```
Chrome (port 54321) ──┐
Spotify (port 54322) ─┤  Transport Layer (Mux) ──→ Network Layer ──→ Internet
Slack (port 54323) ───┘
```

### 3.2 Demultiplexing (Receiver Side)

The transport layer **receives segments** from the network layer and delivers each to the correct application process based on the port number.

```
Internet ──→ Network Layer ──→ Transport Layer (Demux) ──┬─→ Chrome (:80)
                                                          ├─→ Spotify (:8080)
                                                          └─→ Slack (:443)
```

### 3.3 How Demultiplexing Works

The OS looks at the **4-tuple** in the segment header to identify the correct socket:

```
4-Tuple = (Source IP, Source Port, Dest IP, Dest Port)

Incoming segment: (142.250.68.46, 443, 192.168.1.10, 54321)
OS looks for socket: dest_port=54321 → routes to Chrome tab ✅

Different segment: (142.250.68.46, 443, 192.168.1.10, 54322)
→ routes to Chrome's other tab (different source port) ✅
```

**TCP demultiplexing** uses all 4 fields (supports many connections from one server).
**UDP demultiplexing** uses only dest IP + dest port (one socket per port).

---

## 4. Segmentation and Reassembly

The Application Layer may produce a large message (e.g., 10MB file). The Transport Layer **segments** this into smaller pieces that fit within network limits.

```
App data: [────────────────── 10 MB ──────────────────]
          ↓ Transport Layer segments it
Segment 1: [HDR|── 1460 bytes ──]  Seq=0
Segment 2: [HDR|── 1460 bytes ──]  Seq=1460
Segment 3: [HDR|── 1460 bytes ──]  Seq=2920
...
Segment N: [HDR|── last bytes  ──]  Seq=9999660

At destination:
Transport Layer reassembles in order → delivers complete 10 MB to app
```

**MSS (Maximum Segment Size):**
- The largest amount of data TCP will send in a single segment
- Typically `MTU − IP header − TCP header = 1500 − 20 − 20 = 1460 bytes`

---

## 5. The Socket — Key Concept

A **socket** is the interface between the application and transport layer. Think of it as a "door" through which data enters and leaves the network stack.

```
Application Layer
      ↕  Socket API (bind, listen, connect, send, recv)
Transport Layer
      ↕  TCP segment / UDP datagram
Network Layer
```

```python
# Server side (Python):
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
s.bind(('0.0.0.0', 8080))   # Bind to port 8080
s.listen(5)                   # Listen for connections
conn, addr = s.accept()       # Accept incoming connection

# Client side:
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('192.168.1.10', 8080))   # Connect to server
c.send(b'Hello!')
```

---

## 6. Transport Layer vs Network Layer

| Aspect | Network Layer (L3) | Transport Layer (L4) |
|--------|-------------------|---------------------|
| **Delivery unit** | Host-to-host | **Process-to-process** |
| **Address used** | IP Address | Port Number |
| **Reliability** | Best-effort | TCP: reliable; UDP: best-effort |
| **Protocol** | IP | TCP, UDP |
| **Scope** | Routers (intermediate nodes) | Only end systems (source + destination) |

> **Key distinction**: Routers only look at the IP header (Layer 3). They do NOT examine TCP/UDP ports. Port-based decisions happen only at the endpoints.

---

## 7. Interview Questions

**Q1: What is the role of the transport layer?**
> The transport layer provides process-to-process (end-to-end) communication between applications on different hosts. It uses port numbers to identify processes, and optionally provides reliability (TCP), flow control, and congestion control. It sits above the network layer (host-to-host) and below the application layer.

**Q2: What is a port number and why is it needed?**
> A port number (16-bit, 0–65535) identifies a specific process or service on a host. The IP address gets a packet to the right machine; the port number gets it to the right process (e.g., port 80 for HTTP, port 443 for HTTPS).

**Q3: What is a socket?**
> A socket is the combination of an IP address and a port number — it uniquely identifies one endpoint of a network connection. A TCP connection is identified by a 4-tuple: (Source IP, Source Port, Dest IP, Dest Port).

**Q4: What is multiplexing and demultiplexing?**
> Multiplexing (sender): combining data streams from multiple application processes into one network stream with port numbers in headers. Demultiplexing (receiver): distributing incoming segments to the correct application process based on destination port (UDP) or the full 4-tuple (TCP).

**Q5: What is MSS?**
> Maximum Segment Size — the maximum amount of data (not including TCP/IP headers) that TCP will put in a single segment. Typically 1460 bytes for Ethernet (MTU 1500 − 20 IP header − 20 TCP header).

---

*Next: [02 — TCP Deep Dive →](./02_TCP_Deep_Dive.md)*
