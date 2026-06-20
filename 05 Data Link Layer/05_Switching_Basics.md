# 🔀 Switching Basics

> **Switching** = The mechanism by which a network transfers data from a source to a destination across interconnected nodes.

---

## 1. What is Switching?

A **switch** (or switching device) is a node that receives data, makes a forwarding decision based on an address, and sends the data toward its destination.

```
Source ──→ Node 1 ──→ Node 2 ──→ Node 3 ──→ Destination
               ↑         ↑         ↑
           Switching Switching Switching
```

There are three fundamental switching techniques:

```
Switching Techniques
├── Circuit Switching
├── Packet Switching
└── Message Switching
```

---

## 2. Circuit Switching

### 2.1 Concept

A **dedicated physical path** is established between the sender and receiver **before** communication begins. The path remains reserved for the entire duration of the communication.

```
Setup Phase:   A ──→ Request ──→ B  (path reserved)
Transfer Phase: A ══════════════ B  (data flows on dedicated path)
Teardown Phase: A ──→ Release ──→ B  (path freed)
```

### 2.2 How It Works

1. **Call Setup**: Source sends a setup request through the network. Each intermediate node reserves a channel (bandwidth) for this connection.
2. **Data Transfer**: Data flows continuously on the dedicated path — no addressing needed per packet.
3. **Call Teardown**: After communication, the reserved resources are released.

```
Network:    A ── [Router1] ── [Router2] ── B
Circuit:    A ════════════════════════════ B  (dedicated link reserved)
```

### 2.3 Advantages

| Advantage | Description |
|-----------|-------------|
| **Guaranteed bandwidth** | Dedicated resources = predictable performance |
| **No delay variation** | Fixed path, no queuing delays |
| **Simple data transfer** | No addressing overhead per packet |
| **Real-time suitable** | Good for voice calls |

### 2.4 Disadvantages

| Disadvantage | Description |
|-------------|-------------|
| **Channel wastage** | Resources reserved even when no data is sent (idle time) |
| **Setup delay** | Must establish connection before any data can flow |
| **Inflexible** | If a node fails, entire call drops |
| **Expensive** | Dedicated resources are costly |

### 2.5 Real-World Example

- **Traditional telephone network (PSTN)** — when you call someone, a circuit is established through multiple telephone exchanges for the duration of the call.
- **ISDN** (Integrated Services Digital Network)

---

## 3. Packet Switching

### 3.1 Concept

Data is broken into small chunks called **packets**. Each packet is transmitted independently through the network, potentially taking **different routes**, and reassembled at the destination.

```
Message: "HELLO WORLD"
Split into packets:
  [HELLO][Hdr] ──→ may go through Route A
  [ WOR ][Hdr] ──→ may go through Route B
  [ LD  ][Hdr] ──→ may go through Route A or B
```

Each packet contains:
- **Header**: Source IP, Dest IP, sequence number, etc.
- **Payload**: Actual data chunk

### 3.2 How It Works

```
Source              Router 1           Router 2           Dest
  │                    │                  │                 │
  │──[Pkt 1]──────────→│                  │                 │
  │──[Pkt 2]──────────→│──[Pkt 1]────────→│──[Pkt 1]───────→│
  │──[Pkt 3]──────────→│──[Pkt 2]────────→│──[Pkt 2]───────→│
                        │──[Pkt 3]────────→│──[Pkt 3]───────→│
                                                             │
                                                      Reassemble!
```

### 3.3 Two Modes of Packet Switching

#### A. Datagram (Connectionless)
- **No path setup** — each packet is forwarded independently based on routing tables.
- Packets may take **different paths** and arrive **out of order**.
- Destination must **reorder** packets.
- **More robust** — if a router fails, packets find alternate routes.
- **Example: IP (Internet Protocol)**

```
Packet 1 ──→ Router A ──→ Router C ──→ Destination
Packet 2 ──→ Router B ──→ Router D ──→ Destination
(different paths, arrive out of order)
```

#### B. Virtual Circuit (Connection-Oriented)
- A **logical path is set up** before data transfer (like circuit switching, but resources are NOT dedicated).
- All packets follow the **same predetermined path**.
- Packets arrive in order.
- **Example: ATM, Frame Relay, MPLS**

```
Setup: Source ──→ VC established ──→ Destination
Data:  All packets follow same path in order
```

### 3.4 Store-and-Forward

In packet switching, each router:
1. **Receives** the entire packet.
2. **Checks** for errors (FCS).
3. **Looks up** the routing table.
4. **Forwards** the packet to the next hop.

This is called **store-and-forward** switching.

```
Store-and-Forward Delay:
  Total transmission time = n × (L/R)
  where: n = number of links, L = packet size, R = link bandwidth

Example:
  3 links, 1000-bit packet, 1 Mbps each:
  Delay = 3 × (1000/1,000,000) = 3 ms
  (not counting propagation delay)
```

### 3.5 Advantages of Packet Switching

| Advantage | Description |
|-----------|-------------|
| **Efficient channel use** | No dedicated reservation; channel shared by many |
| **Fault tolerant** | Alternate routes used if a node fails |
| **No setup required** | Send packets immediately |
| **Variable-length messages** | Easy to handle different data sizes |

### 3.6 Disadvantages of Packet Switching

| Disadvantage | Description |
|-------------|-------------|
| **Variable delay** | Queuing at routers → jitter |
| **Overhead** | Every packet carries header (addressing info) |
| **Out-of-order delivery** | Datagram mode: packets may arrive out of order |
| **Not ideal for real-time** | Delay jitter bad for voice/video (traditionally) |

### 3.7 Queuing Delay

At each router, packets may wait in a queue (buffer) if the outgoing link is busy:

```
Router Buffer:
  ┌─────┐ ┌─────┐ ┌─────┐
  │Pkt3 │ │Pkt2 │ │Pkt1 │──→ Outgoing Link
  └─────┘ └─────┘ └─────┘
    ↑ waiting (queuing delay)
```

If the buffer is **full** → **packet drop** (congestion).

---

## 4. Message Switching

### 4.1 Concept

The **entire message** (not split into packets) is sent to an intermediate node, which **stores it** and then **forwards** it to the next node when the link is available.

Also called **"Store-and-Forward" switching** (historically).

```
Source ──→ Intermediate Store ──→ Another Store ──→ Destination
              (entire message)    (entire message)
```

### 4.2 Characteristics

- Messages can be **very large** (no size limit imposed).
- Each intermediate node stores the **complete message** before forwarding.
- **No dedicated path** needed.
- Suitable for **non-real-time** communication (e.g., email, telegrams).

### 4.3 Advantages

| Advantage | Description |
|-----------|-------------|
| No dedicated path needed | Efficient use of links |
| Can handle messages of any size | Flexible |
| Works during congestion | Messages queued and forwarded when possible |

### 4.4 Disadvantages

| Disadvantage | Description |
|-------------|-------------|
| **Large storage required** | Each node must store entire large messages |
| **High delay** | Long messages block links for other users |
| **Not real-time** | Unsuitable for voice/video |

### 4.5 Real-World Examples

- **Email** (SMTP — store and forward)
- **Telegram systems** (historical)
- **Store-and-forward fax**

---

## 5. Layer 2 Switching (Data Link Layer)

### 5.1 What is a Layer 2 Switch?

A **Layer 2 switch** operates at the Data Link Layer and forwards frames based on **MAC addresses**.

```
Switch Operation:
1. Frame arrives on a port
2. Switch reads the Source MAC → Updates MAC table (port ↔ MAC)
3. Switch reads the Destination MAC → Looks up MAC table
   ├── Found → Forward ONLY to that port
   └── Not Found → Flood to all ports (except incoming)
```

### 5.2 MAC Address Table (CAM Table)

```
┌─────────────────────────────────────────────┐
│          MAC Address Table                  │
├───────────────────┬──────────┬──────────────┤
│   MAC Address     │  Port    │  TTL (timer) │
├───────────────────┼──────────┼──────────────┤
│ AA:BB:CC:DD:EE:01 │  Port 1  │  300 sec     │
│ AA:BB:CC:DD:EE:02 │  Port 2  │  298 sec     │
│ AA:BB:CC:DD:EE:05 │  Port 5  │  250 sec     │
└───────────────────┴──────────┴──────────────┘
```

- MAC table entries **expire** (TTL) to handle device movement.
- On expiry, next frame from that device relearns the port.

### 5.3 Switching Operations

| Operation | When | Action |
|-----------|------|--------|
| **Learning** | Source MAC unknown | Add src MAC → port mapping to table |
| **Forwarding** | Dest MAC known | Send frame to specific port |
| **Flooding** | Dest MAC unknown | Send to all ports except source |
| **Filtering** | Dest is on same port as source | Drop frame (already there) |
| **Aging** | Timer expires | Remove stale MAC entries |

### 5.4 Broadcast vs Collision Domain

```
HUB (Layer 1):
  ┌──────────────────────────────────────┐
  │         ONE Collision Domain          │
  │  PC1 ── HUB ── PC2                   │
  │              ── PC3                   │
  │              ── PC4                   │
  └──────────────────────────────────────┘
  All PCs share bandwidth and collide

SWITCH (Layer 2):
  ┌────────────────────────────────────────┐
  │   Each port = SEPARATE Collision Domain│
  │  PC1 ──│                              │
  │  PC2 ──│ SWITCH ── (shared broadcast) │
  │  PC3 ──│                              │
  │  PC4 ──│                              │
  └────────────────────────────────────────┘
  No collisions between ports, but ONE broadcast domain
```

### 5.5 Spanning Tree Protocol (STP) — Brief Note

When multiple switches are connected in a network, redundant links create **loops** — frames would circulate forever (broadcast storm). **STP (IEEE 802.1D)** prevents this by:
- Electing a **root bridge**
- Blocking redundant paths
- Enabling blocked paths only if the primary path fails

---

## 6. Comparison: All Switching Types

| Feature | Circuit | Packet | Message |
|---------|---------|--------|---------|
| **Path** | Dedicated | Dynamic (per packet) | Dynamic (per message) |
| **Setup needed?** | ✅ Yes | ❌ No (datagram) | ❌ No |
| **Ordering** | In-order | May be out-of-order | Out-of-order possible |
| **Store at node?** | ❌ No | Briefly (buffer) | ✅ Yes (full message) |
| **Bandwidth** | Wasted if idle | Efficient (shared) | Efficient |
| **Delay** | Low (after setup) | Variable | High |
| **Real-time suitable?** | ✅ Best | ✅ Acceptable | ❌ No |
| **Examples** | PSTN, ISDN | Internet (IP) | Email, Telegram |
| **Resource reservation** | Yes | No | No |

---

## 7. Interview Questions

**Q1: What is the difference between circuit switching and packet switching?**
> Circuit switching establishes a dedicated path before communication; resources are reserved. Packet switching splits data into packets sent independently; resources are shared and no dedicated path exists. Packet switching is more efficient; circuit switching has lower latency.

**Q2: What is store-and-forward in packet switching?**
> Each router receives the complete packet, checks for errors, looks up the routing table, and then forwards it. This introduces some delay but allows error checking at each hop.

**Q3: What is the difference between a hub and a switch?**
> A hub (Layer 1) broadcasts all frames to all ports — one collision domain for all devices. A switch (Layer 2) learns MAC addresses and forwards frames only to the correct port — separate collision domains but one broadcast domain.

**Q4: What is flooding and when does a switch do it?**
> When a switch receives a frame with an unknown destination MAC address (not in its MAC table), it sends the frame out of all ports except the incoming port. When the destination responds, the switch learns its MAC.

**Q5: What is a broadcast domain vs. a collision domain?**
> A collision domain is a network segment where simultaneous transmissions cause collisions (each switch port is its own). A broadcast domain is a segment where a broadcast frame is received by all devices (switches don't break broadcast domains — routers do).

**Q6: What is the purpose of STP?**
> Spanning Tree Protocol prevents loops in networks with redundant switch connections. Loops would cause broadcast storms where frames circulate indefinitely. STP blocks redundant paths and enables them only on failure.

**Q7: Why is packet switching preferred over circuit switching for the internet?**
> Packet switching efficiently shares bandwidth among many users — no resources are wasted when there's no data. The internet has bursty traffic, which packet switching handles much better. Circuit switching wastes bandwidth during idle periods.

**Q8: What is the difference between datagram and virtual circuit packet switching?**
> Datagram: each packet forwarded independently, may take different routes, arrive out of order — like IP. Virtual circuit: a path is set up in advance, all packets follow the same path, arrive in order — like ATM or MPLS.

---

*← Back to [Index](./README.md)*
