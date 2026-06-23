#  UDP & TCP vs UDP Comparison

> ⭐ **TCP vs UDP is one of the most asked questions in software engineering interviews.**

---

## 1. UDP — User Datagram Protocol

### 1.1 What is UDP?

**UDP (User Datagram Protocol)** is a **connectionless, unreliable, lightweight** transport protocol. It provides minimal services — just port-based process delivery and an optional checksum. Everything else is the application's responsibility.

```
UDP Philosophy:
  "Fire and forget — send the data, don't worry about whether it arrives."
```

### 1.2 UDP Header (Only 8 Bytes — Fixed!)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├───────────────────────────┬───────────────────────────────────────┤
│     Source Port (16 bits) │     Destination Port (16 bits)        │
├───────────────────────────┼───────────────────────────────────────┤
│       Length (16 bits)    │       Checksum (16 bits)              │
├───────────────────────────┴───────────────────────────────────────┤
│                   Data (payload)                                   │
└───────────────────────────────────────────────────────────────────┘
```

| Field | Size | Purpose |
|-------|------|---------|
| **Source Port** | 16 bits | Sender's port (optional — can be 0) |
| **Destination Port** | 16 bits | Receiver's port |
| **Length** | 16 bits | Length of UDP header + data |
| **Checksum** | 16 bits | Error detection (optional in IPv4, mandatory in IPv6) |

> **UDP header = 8 bytes. TCP header = 20 bytes minimum.** UDP's tiny header means much less overhead.

### 1.3 UDP Features

```
✅ Connectionless      — No handshake, no connection setup
✅ No reliability      — No ACKs, no retransmissions
✅ No ordering         — Datagrams may arrive out of order (or not at all)
✅ No flow control     — Sender can overwhelm receiver
✅ No congestion ctrl  — UDP doesn't slow down for the network
✅ Lightweight         — 8-byte header, minimal processing
✅ Fast                — No setup delay, no retransmission delay
✅ Broadcast/Multicast — Supports one-to-many delivery (TCP cannot)
✅ Message-oriented    — Preserves message boundaries (unlike TCP's stream)
```

### 1.4 UDP is Message-Oriented

Unlike TCP (stream), UDP **preserves message boundaries**:

```
TCP (Stream-oriented):
  Sender sends: send("Hello"), send(" World")
  Receiver gets: recv() → "Hello World" (or "Hell", "o Wo", "rld" — any split!)
  (TCP merges data into a stream, boundaries lost)

UDP (Message-oriented):
  Sender sends: sendto("Hello"), sendto(" World")
  Receiver gets: recvfrom() → "Hello"    (first datagram — complete)
                 recvfrom() → " World"   (second datagram — complete)
  (Each sendto creates one UDP datagram, boundaries preserved)
```

### 1.5 When is UDP Appropriate?

UDP is the right choice when:

1. **Speed matters more than reliability** (e.g., real-time games — a missed position update is irrelevant if the next one arrives)

2. **Application handles its own reliability** (e.g., QUIC, TFTP, some game protocols build reliability on top of UDP)

3. **Low latency is critical** (e.g., VoIP — a retransmitted 100ms-old voice packet is worse than dropping it)

4. **Broadcast/Multicast needed** (e.g., DHCP, mDNS — TCP can't broadcast)

5. **Simple request-reply** (e.g., DNS — one small query, one small reply; TCP's overhead is excessive)

6. **Streaming where loss is acceptable** (e.g., live video — a dropped frame is better than pausing to retransmit)

---

## 2. UDP Applications

| Application | Protocol | Why UDP? |
|------------|---------|---------|
| **DNS** | UDP (port 53) | Small query/response — overhead of TCP handshake is too high |
| **DHCP** | UDP (67/68) | Broadcast needed — TCP can't broadcast |
| **VoIP / Video calls** | UDP (RTP) | Real-time — retransmission useless (old voice packet is worthless) |
| **Video streaming** | UDP (QUIC) | Low latency; loss is handled by codec, not retransmission |
| **Online gaming** | UDP | Position updates are time-sensitive; old updates are useless |
| **TFTP** | UDP (port 69) | Simple file transfer with own ACK mechanism |
| **SNMP** | UDP (161) | Polling — simple request/response |
| **NTP** | UDP (123) | Time sync — small packets, no connection needed |
| **mDNS / Bonjour** | UDP (5353) | Multicast needed |

---

## 3. TCP vs UDP ⭐ VERY IMPORTANT

### 3.1 Full Comparison Table

| Feature | **TCP** | **UDP** |
|---------|:-------:|:-------:|
| **Connection** | Connection-oriented (3-way handshake) | Connectionless (no setup) |
| **Reliability** | ✅ Guaranteed delivery | ❌ Best-effort (may lose) |
| **Ordering** | ✅ In-order delivery | ❌ May arrive out of order |
| **Flow Control** | ✅ rwnd | ❌ None |
| **Congestion Control** | ✅ Slow Start, AIMD | ❌ None |
| **Error Detection** | ✅ Checksum (always) | ✅ Checksum (optional IPv4) |
| **Speed** | Slower (overhead, retransmit) | **Faster** (minimal overhead) |
| **Header size** | 20–60 bytes | **8 bytes (fixed)** |
| **Data type** | Byte stream | **Message (datagram)** |
| **Broadcast/Multicast** | ❌ No | ✅ Yes |
| **Setup delay** | Yes (handshake ~1 RTT) | **None** |
| **State at endpoints** | Stateful (connection state) | Stateless |
| **Throughput** | May be lower under loss | Higher under stable conditions |
| **Latency** | Higher | **Lower** |
| **Use case** | File transfer, web, email, SSH | VoIP, DNS, streaming, gaming |
| **Examples** | HTTP/S, FTP, SMTP, SSH | DNS, DHCP, VoIP, UDP gaming |

### 3.2 Visual Contrast

```
TCP — Connection-oriented:
  Client ─── SYN ──────────→ Server
  Client ←── SYN-ACK ─────── Server    (1 RTT overhead before data!)
  Client ─── ACK ──────────→ Server
  Client ═══ DATA ══════════ Server    (reliable, ordered)
  Client ─── FIN ──────────→ Server    (graceful close)
  ...

UDP — Connectionless:
  Client ─── DATA ──────────→ Server   (immediate! no setup)
  Client ─── DATA ──────────→ Server   (may arrive out of order)
  Client ─── DATA ─────────╳  (lost — nobody knows, nobody retransmits)
```

### 3.3 When to Use Which?

```
Use TCP when:
  ✅ Data must be complete and correct
     (file downloads, web pages, database queries)
  ✅ Order matters
     (SSH, HTTP, email)
  ✅ Loss cannot be tolerated
     (financial transactions, file transfers)

Use UDP when:
  ✅ Low latency matters more than reliability
     (VoIP, video calls, online gaming)
  ✅ Old data is useless (would rather drop than wait for retransmit)
     (live audio/video, stock tickers)
  ✅ Broadcast/multicast needed
     (DHCP discovery, mDNS)
  ✅ Very small queries (overhead of TCP excessive)
     (DNS, SNMP, NTP)
  ✅ Application implements its own reliability
     (QUIC, custom game protocols)
```

### 3.4 The Latency Problem with TCP

```
TCP connection + HTTP request:

T=0ms:    Client → SYN
T=10ms:   Server → SYN-ACK    (10ms one-way delay)
T=20ms:   Client → ACK + HTTP Request
T=30ms:   Server → HTTP Response
T=40ms:   Client receives data

Total: 40ms for first byte (2 RTTs!)

UDP (e.g., DNS):
T=0ms:    Client → DNS Query
T=10ms:   Server → DNS Response
T=20ms:   Client receives answer

Total: 20ms (1 RTT) — much faster for simple queries!
```

---

## 4. QUIC — The Modern "TCP+UDP" Protocol

### 4.1 Why QUIC?

HTTP/3 runs over **QUIC** (Quick UDP Internet Connections) — a protocol built on top of UDP that provides TCP-like reliability with lower latency.

**QUIC solves TCP's biggest problem: Head-of-Line (HoL) Blocking.**

```
TCP Head-of-Line Blocking (HTTP/2):
  Stream 1: [P1][P2][P3]  ← P2 lost!
  Stream 2: [P4][P5][P6]  ← blocked waiting for P2 to be retransmitted!
  Stream 3: [P7][P8][P9]  ← blocked too!

QUIC (each stream independent over UDP):
  Stream 1: [P1][__][P3]  ← P2 lost, retransmitting
  Stream 2: [P4][P5][P6]  ← NOT blocked! Delivers independently ✅
  Stream 3: [P7][P8][P9]  ← NOT blocked! ✅
```

### 4.2 QUIC vs TCP vs UDP

| Feature | TCP | UDP | QUIC |
|---------|-----|-----|------|
| Reliability | ✅ | ❌ | ✅ |
| Connection | ✅ | ❌ | ✅ (0-RTT reconnect) |
| Multiplexing | ❌ (HoL block) | N/A | ✅ Independent streams |
| Encryption | Optional (TLS on top) | No | ✅ Built-in TLS 1.3 |
| Handshake | 1 RTT (+ TLS) | 0 | 1 RTT or 0-RTT |
| OS support | Kernel | Kernel | User-space |
| Used by | HTTP/1.1, HTTP/2 | DNS, games | HTTP/3 |

---

## 5. UDP Reliability — Application-Level Solutions

When you need reliability over UDP (e.g., game networking, QUIC):

```
Application implements:
  1. Sequence numbers  → detect out-of-order/missing packets
  2. Selective ACKs    → confirm received packets
  3. Retransmission    → resend lost packets
  4. Timeout/backoff   → don't flood on retransmit

This gives you selective reliability — you choose WHAT to make reliable,
unlike TCP which makes EVERYTHING reliable.

Example: In a game:
  Position updates → UDP, no reliability (latest one is enough)
  Chat messages    → Reliable UDP (must arrive) or TCP
  Item pickups     → Reliable UDP (critical game state)
```

---

## 6. TCP & UDP Interview Scenarios

### Scenario 1: File Transfer
```
Use TCP ✅
  - File must arrive complete and correct
  - A single corrupted bit makes the file unusable
  - Slight delay acceptable
```

### Scenario 2: Video Streaming (YouTube, Netflix)
```
Use TCP (HTTP) or QUIC ✅
  - Buffering allows TCP's retransmission
  - Quality adapts to bandwidth (adaptive bitrate)
  - But QUIC (UDP-based) gives better multiplexing

Note: LIVE streaming (Twitch) might use UDP/RTMP
  - Can't wait for retransmit
  - Dropped frames acceptable
```

### Scenario 3: Online Gaming
```
Use UDP ✅
  - Position/state updates are time-sensitive
  - 100ms retransmit > just show next position
  - Low latency is critical
  - Application handles reliability for critical events (pickups, damage)
```

### Scenario 4: DNS Query
```
Use UDP ✅
  - Small request + small response (fits in one datagram)
  - TCP handshake overhead > benefit
  - If UDP times out, DNS client retries
  - DNS uses TCP for responses > 512 bytes (zone transfers)
```

### Scenario 5: SSH / Remote Terminal
```
Use TCP ✅
  - Every character must arrive in order
  - A dropped character = corrupted terminal session
  - Latency is acceptable
```

### Scenario 6: Voice over IP (WhatsApp/Zoom call)
```
Use UDP (RTP) ✅
  - A 100ms late audio packet is useless
  - Rather drop a few milliseconds of audio than add 200ms delay
  - Jitter buffer at receiver handles small variations
  - Application-layer error concealment handles loss
```

---

## 7. Summary: Key Numbers to Remember

| | TCP | UDP |
|--|-----|-----|
| Header | **20** bytes min | **8** bytes (always) |
| Max header | 60 bytes (with options) | 8 bytes |
| Port range | 0–65535 | 0–65535 |
| Handshake | 3-way SYN | None |
| Teardown | 4-way FIN | None |
| Window | 16-bit (64KB), extended with WSCALE | No window |

---

## 8. Interview Questions

**Q1: What are the main differences between TCP and UDP?**
> TCP is connection-oriented (3-way handshake), reliable (ACKs, retransmission), ordered, has flow and congestion control, 20-byte header, slower but guaranteed. UDP is connectionless, unreliable (best-effort), unordered, no flow/congestion control, 8-byte header, faster but no delivery guarantee.

**Q2: When would you choose UDP over TCP?**
> When low latency is critical and loss is acceptable (VoIP, live streaming, gaming), when the application implements its own reliability (QUIC), for broadcast/multicast (DHCP, mDNS), or for simple one-shot request-replies where TCP's handshake overhead is excessive (DNS, NTP, SNMP).

**Q3: Can UDP be reliable?**
> UDP itself has no reliability, but applications can implement reliability on top of UDP — sequence numbers, ACKs, retransmissions. QUIC does this. This gives selective reliability: you choose which data must be reliable, with lower overhead than TCP's universal reliability.

**Q4: Why does DNS use UDP?**
> DNS queries and responses are typically small (fit in one datagram). TCP's 3-way handshake would add 1 RTT of latency before the query even starts — doubling the lookup time. If the UDP response is lost, the DNS client simply retries. DNS falls back to TCP only for large responses (>512 bytes) or zone transfers.

**Q5: What is head-of-line blocking in TCP?**
> Since TCP delivers bytes in order, if a segment is lost, all subsequent segments (even if received) must wait for the retransmitted segment. In HTTP/2 multiplexed streams over TCP, one lost packet blocks ALL streams in the connection — not just the one stream that lost data. QUIC (HTTP/3) solves this by multiplexing independent streams over UDP.

**Q6: Why is UDP connectionless better for streaming?**
> Streaming requires low latency. TCP's retransmissions add delay — by the time a lost audio packet is retransmitted, it's too late to play it. UDP's "best-effort" means audio plays with occasional glitches (handled by jitter buffers and error concealment) rather than freezing while TCP retransmits. Older audio is useless; UDP never wastes time on it.

**Q7: What is the UDP checksum and is it mandatory?**
> The UDP checksum provides error detection (like TCP/IP checksums — 1's complement sum). In IPv4, it's OPTIONAL (all-zeros means no checksum). In IPv6, it's MANDATORY because IPv6 headers don't have a checksum. In practice, most implementations compute it for reliability.

**Q8: How large can a UDP datagram be?**
> The UDP length field is 16 bits → max 65,535 bytes total (header + data) → max 65,527 bytes of data. But this is limited further by IP fragmentation (IPv4 max datagram = 65,535 bytes) and practical MTU (1472 bytes data for Ethernet to avoid fragmentation). QUIC typically sends smaller packets.

---

*← Back to [Index](./README.md)*
