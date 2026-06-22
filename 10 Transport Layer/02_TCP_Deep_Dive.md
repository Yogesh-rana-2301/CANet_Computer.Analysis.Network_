# 🔗 TCP — Transmission Control Protocol (Deep Dive)

> ⭐ **VERY HIGH PRIORITY** — TCP is one of the most important protocols in all of networking. Know this inside-out.

---

## 1. TCP Overview

**TCP (Transmission Control Protocol)** provides **reliable, ordered, connection-oriented** byte-stream delivery between two processes.

### TCP's Core Guarantees:
```
✅ Reliable     — Every byte sent is received (no loss, no corruption)
✅ Ordered      — Bytes delivered to application in exact order sent
✅ Full-duplex  — Both sides can send and receive simultaneously
✅ Connection   — Explicit setup and teardown (handshakes)
✅ Flow Control — Sender won't overwhelm receiver
✅ Congestion   — Sender won't overwhelm the network
```

### TCP Header (20 bytes minimum):
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├───────────────────────┬──────────────────────────────────────────┤
│    Source Port (16)   │         Destination Port (16)            │
├───────────────────────┴──────────────────────────────────────────┤
│                    Sequence Number (32 bits)                      │
├──────────────────────────────────────────────────────────────────┤
│                 Acknowledgement Number (32 bits)                  │
├────────┬──────────┬──┬──┬──┬──┬──┬──┬──────────────────────────┤
│DataOff │ Reserved │ U│ A│ P│ R│ S│ F│     Window Size (16)      │
│ (4)    │   (6)    │ R│ C│ S│ S│ Y│ I│                           │
│        │          │ G│ K│ H│ T│ N│ N│                           │
├────────┴──────────┴──┴──┴──┴──┴──┴──┴──────────────────────────┤
│           Checksum (16)           │     Urgent Pointer (16)      │
├───────────────────────────────────┴──────────────────────────────┤
│                   Options (0–40 bytes, if DataOffset > 5)        │
└──────────────────────────────────────────────────────────────────┘
```

**Key TCP Header Fields:**
| Field | Size | Purpose |
|-------|------|---------|
| **Source Port** | 16 bits | Sender's port |
| **Destination Port** | 16 bits | Receiver's port |
| **Sequence Number** | 32 bits | Byte offset of first byte in segment |
| **Acknowledgement Number** | 32 bits | Next byte expected from other side |
| **Data Offset (Header Length)** | 4 bits | Header length in 32-bit words |
| **Flags** | 6 bits | SYN, ACK, FIN, RST, PSH, URG |
| **Window Size** | 16 bits | Flow control — receive buffer space |
| **Checksum** | 16 bits | Error detection |

**TCP Flags:**
| Flag | Name | Meaning |
|------|------|---------|
| **SYN** | Synchronize | Initiate connection, exchange ISN |
| **ACK** | Acknowledge | Acknowledges received data |
| **FIN** | Finish | Initiates connection termination |
| **RST** | Reset | Abort connection immediately |
| **PSH** | Push | Push data to application immediately |
| **URG** | Urgent | Urgent data (rarely used) |

---

## 2. Sequence Numbers and ACKs ⭐

### 2.1 Sequence Numbers

TCP views data as a **stream of bytes**. The **Sequence Number (SeqNum)** in a segment's header identifies the **byte offset** of the first byte in that segment within the overall byte stream.

```
Application data: "HELLO WORLD" (11 bytes)
Initial Seq Num (ISN): 1000 (randomly chosen during handshake)

Segment 1: SeqNum=1000, Data="HEL" (3 bytes)
Segment 2: SeqNum=1003, Data="LO " (3 bytes)
Segment 3: SeqNum=1006, Data="WOR" (3 bytes)
Segment 4: SeqNum=1009, Data="LD"  (2 bytes)
```

### 2.2 Acknowledgement Numbers

The **ACK number** tells the sender: **"I have received all bytes up to and including byte X−1. Send me byte X next."**

```
Receiver gets Segment 1 (SeqNum=1000, 3 bytes):
  Receiver sends ACK: AckNum=1003  ("I got through byte 1002, send 1003 next")

Receiver gets Segment 2 (SeqNum=1003, 3 bytes):
  Receiver sends ACK: AckNum=1006

Receiver gets Segment 3 (SeqNum=1006, 3 bytes):
  Receiver sends ACK: AckNum=1009
```

> **ACK number = sequence number of NEXT expected byte**

### 2.3 Cumulative ACKs

TCP uses **cumulative acknowledgment** — one ACK acknowledges all bytes up to that point:

```
Sender sends:   Seg1(Seq=100), Seg2(Seq=200), Seg3(Seq=300)
Receiver gets:  Seg1, Seg3 (Seg2 is lost)

ACK behavior:
  After Seg1: ACK=200 (cumulative: all bytes through 199 received)
  After Seg3: ACK=200 (still! Gap at 200: can't ACK beyond the gap)

Sender sees duplicate ACK=200 → knows Seg2 was lost → retransmits Seg2
```

### 2.4 Initial Sequence Number (ISN)

The ISN is **randomly chosen** at connection setup for security:
- Prevents old packets from previous connections being accepted as valid
- Makes it harder for attackers to inject forged segments

---

## 3. Three-Way Handshake ⭐

### 3.1 Why a Handshake?

Before exchanging data, TCP must:
1. Verify both sides are reachable and ready
2. **Synchronize** sequence numbers (so both sides know where the other's byte stream starts)
3. Exchange capabilities (window size, MSS, etc.)

### 3.2 The Three Steps

```
Client                                        Server
  │                                               │
  │  Step 1: SYN                                  │
  │  [SYN=1, SeqNum=x]                            │
  │──────────────────────────────────────────────→│
  │  Client picks random ISN = x                  │
  │  Client enters SYN_SENT state                 │
  │                                               │ Server enters SYN_RCVD state
  │  Step 2: SYN-ACK                              │
  │  [SYN=1, ACK=1, SeqNum=y, AckNum=x+1]        │
  │←─────────────────────────────────────────────│
  │  Server picks own ISN = y                     │
  │  Server acknowledges client: AckNum=x+1       │
  │  ("Got your SYN, expecting byte x+1 next")    │
  │                                               │
  │  Step 3: ACK                                  │
  │  [ACK=1, SeqNum=x+1, AckNum=y+1]             │
  │──────────────────────────────────────────────→│
  │  Client acknowledges server: AckNum=y+1       │
  │  Client enters ESTABLISHED state              │
  │                               Server enters ESTABLISHED state
  │                                               │
  │═══════════ DATA EXCHANGE ═══════════════════ │
```

### 3.3 Why THREE steps (not two)?

Two-way would only confirm one direction. Three-way ensures **both directions** are confirmed:
- Step 1 (SYN): Client → Server connection verified ✅
- Step 2 (SYN-ACK): Server → Client connection verified ✅ + server acknowledges client
- Step 3 (ACK): Client confirms it received server's ISN ✅

### 3.4 Concrete Example with Numbers

```
Client ISN = 1000, Server ISN = 5000

Step 1 — Client sends SYN:
  SYN=1, ACK=0
  SeqNum = 1000
  AckNum = 0 (no ACK yet)

Step 2 — Server sends SYN-ACK:
  SYN=1, ACK=1
  SeqNum = 5000         ← Server's ISN
  AckNum = 1001         ← 1000 + 1 (consumed 1 byte for SYN)

Step 3 — Client sends ACK:
  SYN=0, ACK=1
  SeqNum = 1001         ← Client's next byte (SYN consumed seq 1000)
  AckNum = 5001         ← 5000 + 1 (consumed 1 byte for server's SYN)

Connection ESTABLISHED!
```

> **SYN and FIN each consume one sequence number** even though they carry no data.

### 3.5 TCP States During Handshake

```
Client:  CLOSED → SYN_SENT → ESTABLISHED
Server:  CLOSED → LISTEN → SYN_RCVD → ESTABLISHED
```

### 3.6 SYN Flood Attack

An attacker sends many SYN packets with spoofed source IPs:
```
Attacker → Server: SYN (fake src IP 1.2.3.4)
Server → 1.2.3.4: SYN-ACK (never received — ghost IP)
Server waits for ACK... (allocates memory for half-open connection)

Repeat millions of times → Server's connection table full → DoS!
```

**Defense: SYN Cookies** — server encodes state in the SYN-ACK's sequence number; no memory allocated until valid ACK received.

---

## 4. Four-Way Termination ⭐

### 4.1 Why Four Steps?

TCP connections are **full-duplex** — each direction is independent. Closing one direction doesn't close the other. Each side must send its own FIN and receive an ACK.

```
Client                                        Server
  │                                               │
  │  Step 1: FIN (client done sending)            │
  │  [FIN=1, ACK=1, SeqNum=x]                    │
  │──────────────────────────────────────────────→│
  │  Client enters FIN_WAIT_1                     │
  │                                               │
  │  Step 2: ACK (server acknowledges client FIN) │
  │  [ACK=1, AckNum=x+1]                         │
  │←─────────────────────────────────────────────│
  │  Client enters FIN_WAIT_2                     │
  │  Server enters CLOSE_WAIT                     │
  │                                               │
  │  (Server can still send data here!)           │
  │                                               │
  │  Step 3: FIN (server done sending)            │
  │  [FIN=1, ACK=1, SeqNum=y]                    │
  │←─────────────────────────────────────────────│
  │                          Server enters LAST_ACK│
  │                                               │
  │  Step 4: ACK (client acknowledges server FIN) │
  │  [ACK=1, AckNum=y+1]                         │
  │──────────────────────────────────────────────→│
  │  Client enters TIME_WAIT (waits 2×MSL)        │
  │                            Server enters CLOSED│
  │                                               │
  │ (Client enters CLOSED after 2×MSL timeout)    │
```

### 4.2 TIME_WAIT State

After sending the final ACK, the client waits for **2 × MSL (Maximum Segment Lifetime)** before fully closing:

- **MSL** = maximum time a TCP segment can exist in the network (typically 60–120 seconds)
- **2×MSL reason 1**: If the final ACK is lost, the server will retransmit FIN. Client must still be alive to re-send the ACK.
- **2×MSL reason 2**: Ensures all old duplicate segments from this connection have expired before a new connection reuses the same 4-tuple.

```
TIME_WAIT duration = 2 × MSL = typically 60s – 240s
(Can cause "address already in use" errors when restarting servers!)
```

### 4.3 TCP State Machine (Full)

```
                    CLOSED
                       │
           passive open │ active open (connect())
           (listen())   │
                        ▼
                    SYN_SENT ←──── send SYN
             ┌──→  LISTEN
             │         │ SYN received → send SYN-ACK
             │         ▼
             │     SYN_RCVD
             │         │ ACK received
             │         ▼
             └── ESTABLISHED  ←─────── recv SYN-ACK, send ACK
                      │
                      │ (close — send FIN)
                      ▼
                  FIN_WAIT_1
                      │ ACK received
                      ▼
                  FIN_WAIT_2
                      │ FIN received → send ACK
                      ▼
                  TIME_WAIT
                      │ 2×MSL timeout
                      ▼
                    CLOSED
```

---

## 5. Sliding Window Protocol ⭐

### 5.1 The Problem with Stop-and-Wait

In stop-and-wait: send 1 segment → wait for ACK → send next.

```
Sender: [Seg1] ─────→ (waits...) [Seg2] ─────→ ...
            ← ACK ←              ← ACK ←

Channel utilization = (L/R) / (L/R + RTT) ← Very low for long RTTs!

Example: 1ms transmission, 50ms RTT
  Efficiency = 1 / (1 + 50) = ~2% ← Terrible!
```

### 5.2 Sliding Window Solution

The sender can have **multiple segments in-flight** simultaneously — up to a **window size (W)** of unacknowledged segments.

```
Window size = W = 4 segments

Sender buffer:
  Sent & ACKed │ Sent, unACKed (window) │ Not yet sent │ No data
  [1][2][3][4] │ [5] [6] [7] [8]        │ [9][10]...   │

  As ACKs arrive, the window slides forward:
  [1][2][3][4][5] │ [6] [7] [8] [9]      │ [10][11]...  │ (window slid!)
```

```
Channel utilization = W × (L/R) / (L/R + RTT)

For W=50, L/R=1ms, RTT=50ms:
  Utilization = 50 × 1 / (1 + 50) ≈ 98% ← Excellent!
```

### 5.3 Go-Back-N (GBN)

- Sender can have up to **N** unACKed segments
- If segment k is lost: **retransmit k AND all subsequent segments** (k, k+1, k+2, ...)
- Receiver only accepts in-order segments (discards out-of-order)

```
Window N=4:
Sender: Seg1, Seg2, Seg3, Seg4 → (Seg2 lost!)
Receiver: Gets Seg1 ✅, Seg2 ✗, discards Seg3 Seg4 (out of order)
Receiver ACKs: ACK1, ACK1, ACK1, ACK1 (repeated ACK for last good)
Sender: Sees repeated ACK1 → retransmit Seg2, Seg3, Seg4 (go back to 2)
```

### 5.4 Selective Repeat (SR)

- Sender retransmits **only** the lost/corrupted segment
- Receiver **buffers out-of-order** segments
- More efficient but requires more buffer space

```
Window N=4:
Sender: Seg1, Seg2, Seg3, Seg4 → (Seg2 lost!)
Receiver: Gets Seg1 ✅, Seg2 ✗, buffers Seg3 Seg4
Receiver ACKs: ACK1, NAK2 (or timeout), ACK3, ACK4
Sender: Retransmits only Seg2
Receiver: Delivers Seg1, Seg2, Seg3, Seg4 in order ✅
```

**TCP uses a hybrid** — cumulative ACKs + selective retransmission (SACK option).

---

## 6. Flow Control ⭐

### 6.1 The Problem

The sender might be fast, the receiver might be slow. Without flow control, the receiver's buffer overflows and data is lost.

```
Fast Sender (10 Gbps) → ──────────────── Slow App (reads 100 Mbps)
                         ↑ Buffer fills up and overflows! Data lost!
```

### 6.2 Receive Window (rwnd)

TCP flow control uses the **Receive Window (rwnd)** field in the TCP header — the receiver tells the sender how much buffer space it has available.

```
Receiver's buffer:
  [─────── 4096 bytes total buffer ────────]
  [─── 2048 used (not yet read by app) ────][─── 2048 free ───]

Receiver sends ACK: rwnd = 2048  ← "I can accept 2048 more bytes"

Sender: must keep (last byte sent − last byte ACKed) ≤ rwnd
```

### 6.3 Flow Control in Action

```
Step 1: Receiver has 4096 bytes buffer, all empty
  → Sends rwnd = 4096

Step 2: Sender sends 4096 bytes of data

Step 3: App at receiver has only read 2048 bytes
  → Buffer: 2048 used, 2048 free
  → ACK with rwnd = 2048

Step 4: Sender sends 2048 more bytes (fills remaining window)

Step 5: App hasn't read anything more, buffer full
  → ACK with rwnd = 0  ← STOP! Zero window!

Step 6: Sender pauses (but sends periodic Window Probes)
  → Sender sends 1-byte probe segments to check if window opened

Step 7: App reads 2048 bytes
  → ACK with rwnd = 2048  ← Window reopens!
```

```
         Sender                    Receiver
           │                          │
           │── Data (2000B) ─────────→│  rwnd = 2048
           │── Data (2000B) ─────────→│  rwnd = 48 (almost full)
           │                          │
           │←── ACK, rwnd=0 ─────────│  STOP!
           │                          │
           │── Window Probe (1B) ────→│  (periodic check)
           │←── ACK, rwnd=0 ─────────│  (still full)
           │                          │
           │── Window Probe ─────────→│
           │←── ACK, rwnd=4096 ──────│  App drained the buffer!
           │                          │
           │── Data (4096B) ─────────→│  Resume sending
```

---

## 7. Congestion Control ⭐

### 7.1 Flow Control vs Congestion Control

| | Flow Control | Congestion Control |
|--|-------------|-------------------|
| **Problem** | Receiver's buffer overflow | Network's buffers overflow |
| **Controlled by** | rwnd (receive window) | cwnd (congestion window) |
| **Informed by** | Receiver (rwnd in ACK) | Network (packet loss, ECN) |
| **Protects** | Receiver | Network routers |

### 7.2 Congestion Window (cwnd)

TCP maintains a **congestion window (cwnd)** at the sender:

```
Effective sending rate = min(cwnd, rwnd)
Bytes in flight ≤ min(cwnd, rwnd)
```

**How TCP detects congestion:**
1. **Timeout** — no ACK received within RTT timeout → serious congestion
2. **3 Duplicate ACKs** — ACK for same seq received 3 times → mild congestion (packet lost but network alive)

### 7.3 Slow Start ⭐

**Slow Start** is the initial phase — rapidly grow cwnd from 1 MSS until congestion is detected or **ssthresh (slow start threshold)** is reached.

```
Initial: cwnd = 1 MSS, ssthresh = 64 MSS (or last congestion point)

Round 1: Send 1 MSS → receive ACK → cwnd = 2 MSS  (double!)
Round 2: Send 2 MSS → receive 2 ACKs → cwnd = 4 MSS (double!)
Round 3: Send 4 MSS → receive 4 ACKs → cwnd = 8 MSS
Round 4: cwnd = 16 MSS
...

Pattern: cwnd grows EXPONENTIALLY (doubles each RTT)
Stops when: cwnd reaches ssthresh → switch to Congestion Avoidance
```

```
cwnd
 64 │                    ╭─── ssthresh
    │                   ╱
 32 │                  ╱
 16 │                ╱     ← Exponential growth (Slow Start)
  8 │             ╱
  4 │          ╱
  2 │       ╱
  1 │────╱
    └───────────────────────→ RTT
     Start     ssthresh reached
```

> **"Slow Start" is a misleading name** — it starts slow (1 MSS) but grows exponentially fast!

### 7.4 Congestion Avoidance — AIMD ⭐

Once cwnd ≥ ssthresh, TCP enters **Congestion Avoidance** (also called **AIMD — Additive Increase, Multiplicative Decrease**).

**Additive Increase:**
- Increase cwnd by **1 MSS per RTT** (linear growth — much slower than Slow Start)
- For each ACK: `cwnd += MSS × (MSS / cwnd)` (roughly 1 MSS per RTT)

```
cwnd = 8 MSS at ssthresh:
After RTT 1: cwnd = 9 MSS
After RTT 2: cwnd = 10 MSS
After RTT 3: cwnd = 11 MSS   ← linear growth
...
```

**Multiplicative Decrease:**
- On **timeout** (severe congestion): `ssthresh = cwnd/2`, `cwnd = 1 MSS` (restart Slow Start)
- On **3 duplicate ACKs** (mild, TCP Reno): `ssthresh = cwnd/2`, `cwnd = cwnd/2` (Fast Recovery)

```
cwnd
    │            ╭─────────────── Congestion
    │           ╱                 Avoidance (linear)
    │          ╱
    │         ╱ ssthresh
    │        ╱/─────────────
    │      ╱╱   ↑ Exponential (Slow Start)
    │    ╱╱
    │──╱╱
    └────────────────────────→ RTT
```

### 7.5 Full AIMD/Congestion Control Picture

```
cwnd
(MSS)
 16 │                        *
    │                       ╱│
    │                      ╱ │ 3 dup ACKs detected!
    │                     ╱  │ ssthresh = 16/2 = 8
  8 │           *        ╱   │ cwnd = 8
    │          ╱│       ╱    │
    │         ╱ │  AI  ╱     │  *
    │        ╱  │─────       │ ╱│ Timeout!
    │       ╱   └─────────── ssthresh=8
    │      ╱                 │ cwnd=1
  4 │    ╱ Slow Start        │
    │   ╱                    │
  2 │  ╱                     │ Slow Start again
    │ ╱                      │╱
  1 │╱                       │
    └────────────────────────────────────→ time
       Conn   ssthresh  AI   Congestion  Restart
       start  reached  growth detected
```

### 7.6 TCP Tahoe vs TCP Reno vs TCP CUBIC

| Event | TCP Tahoe | TCP Reno | TCP CUBIC |
|-------|-----------|----------|-----------|
| **On Timeout** | ssthresh=cwnd/2, cwnd=1 | ssthresh=cwnd/2, cwnd=1 | ssthresh=cwnd×0.7, cwnd=1 |
| **On 3 dup ACKs** | ssthresh=cwnd/2, cwnd=1 | ssthresh=cwnd/2, cwnd=ssthresh (Fast Recovery) | Cubic function |
| **Growth** | Slow Start → AI | Slow Start → AI | Cubic function (faster at high BW) |
| **Status** | Legacy | Classic | **Modern Linux default** |

### 7.7 Fast Retransmit

Instead of waiting for timeout (which is slow), TCP can retransmit after **3 duplicate ACKs**:

```
Sender: Seg1, Seg2, Seg3, Seg4, Seg5 → (Seg2 lost!)
Receiver: Gets Seg1 → ACK2
          Gets Seg3 → ACK2 (dup)   ← 1st duplicate
          Gets Seg4 → ACK2 (dup)   ← 2nd duplicate
          Gets Seg5 → ACK2 (dup)   ← 3rd duplicate

Sender: 3 dup ACKs received! → Retransmit Seg2 immediately (Fast Retransmit)
        Don't wait for timeout → much faster recovery!
```

---

## 8. Retransmission Timeout (RTO)

TCP uses an adaptive timeout — it estimates RTT and sets:

$$RTO = \text{EstimatedRTT} + 4 \times \text{DevRTT}$$

Where:
- **EstimatedRTT** = Exponentially weighted moving average (EWMA) of RTT
- **DevRTT** = EWMA of deviation in RTT

$$\text{EstimatedRTT} = (1 - \alpha) \times \text{EstimatedRTT} + \alpha \times \text{SampleRTT}$$
$$\text{DevRTT} = (1 - \beta) \times \text{DevRTT} + \beta \times |\text{SampleRTT} - \text{EstimatedRTT}|$$

Typical: α = 0.125, β = 0.25

**On timeout**: Double the RTO (exponential backoff) until ACK received.

---

## 9. TCP Connection States Summary

| State | Who | Meaning |
|-------|-----|---------|
| `CLOSED` | Both | No connection exists |
| `LISTEN` | Server | Waiting for incoming SYN |
| `SYN_SENT` | Client | SYN sent, waiting for SYN-ACK |
| `SYN_RCVD` | Server | SYN-ACK sent, waiting for ACK |
| `ESTABLISHED` | Both | Connection open, data flowing |
| `FIN_WAIT_1` | Closer | FIN sent, waiting for ACK |
| `FIN_WAIT_2` | Closer | ACK received, waiting for server's FIN |
| `CLOSE_WAIT` | Other | FIN received from closer, app can still send |
| `LAST_ACK` | Other | FIN sent, waiting for final ACK |
| `TIME_WAIT` | Closer | Waiting 2×MSL before truly closed |

---

## 10. Interview Questions

**Q1: Explain TCP's 3-way handshake.**
> Client sends SYN (with its ISN=x). Server responds SYN-ACK (with its ISN=y, AckNum=x+1). Client sends ACK (AckNum=y+1). This verifies both directions and synchronizes sequence numbers. Three steps are needed so both sides confirm the other can send AND receive.

**Q2: Why is the TCP handshake 3-way and not 2-way?**
> A 2-way handshake would only confirm one direction. The third step (client's ACK) confirms to the server that its SYN-ACK was received and the server's initial sequence number is acknowledged. Without it, the server can't be sure the client received its ISN.

**Q3: Why does TCP use a 4-way termination?**
> TCP is full-duplex — each direction is closed independently. When client sends FIN, server ACKs it (half-close). The server can still send data. When server is done, it sends its own FIN. Client ACKs it. Four messages are needed to close both directions of the full-duplex connection.

**Q4: What is the purpose of TIME_WAIT?**
> TIME_WAIT (2×MSL) serves two purposes: 1) If the final ACK is lost, the server will retransmit FIN; the client must still be alive to re-ACK it. 2) Ensures all segments from this connection expire before a new connection reuses the same 4-tuple (avoids old duplicate segments confusing new connections).

**Q5: What is the difference between flow control and congestion control?**
> Flow control prevents the sender from overwhelming the receiver's buffer (uses rwnd — receive window). Congestion control prevents the sender from overwhelming the network's routers (uses cwnd — congestion window). The effective window = min(rwnd, cwnd).

**Q6: Explain Slow Start.**
> Slow Start begins with cwnd=1 MSS. For each ACK received, cwnd increases by 1 MSS — effectively doubling cwnd per RTT (exponential growth). This continues until cwnd reaches ssthresh, after which congestion avoidance (linear growth) takes over. Despite the name, Slow Start grows rapidly.

**Q7: What is AIMD?**
> Additive Increase, Multiplicative Decrease — the TCP congestion avoidance algorithm. Additive Increase: grow cwnd by 1 MSS per RTT when no congestion. Multiplicative Decrease: halve cwnd when congestion detected (loss). This creates the characteristic TCP sawtooth pattern and ensures fairness among competing flows.

**Q8: What is Fast Retransmit?**
> Instead of waiting for a timeout, TCP retransmits a lost segment upon receiving 3 duplicate ACKs. Three duplicate ACKs indicate the segment after the gap is missing. Fast retransmit allows quicker recovery without waiting for the RTO timer.

**Q9: What is the TCP sequence number range?**
> 32 bits → 0 to 2³²−1 (0 to ~4.3 billion). After 2³² bytes, numbers wrap around. On modern high-speed networks, this can wrap quickly (with TCP PAWS — Protection Against Wrapped Sequences — to handle this).

**Q10: What are SYN cookies?**
> A defense against SYN flood attacks. Instead of allocating memory for each half-open connection, the server encodes the connection parameters into the SYN-ACK's sequence number (a cryptographic hash). Only when a valid ACK arrives does the server allocate resources. Prevents memory exhaustion from SYN floods.

---

*Next: [03 — UDP & TCP vs UDP Comparison →](./03_UDP_and_Comparison.md)*
