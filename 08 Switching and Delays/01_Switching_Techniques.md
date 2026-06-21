# 🔀 Switching Techniques

> **Switching** is the mechanism that determines how data moves from a source to a destination through intermediate nodes in a network.

---

## 1. Overview of Switching

A network is a collection of nodes (routers, switches) connected by links. When data must travel from source to destination across multiple hops, the network must decide:
- **Which path** does the data take?
- **How is it stored** at intermediate nodes?
- **When does it move** to the next node?

These decisions define the switching technique.

```
Source ──→ Node 1 ──→ Node 2 ──→ Node 3 ──→ Destination
                ↑         ↑         ↑
            Switching decision at each node
```

**Three fundamental approaches:**
```
┌──────────────────────────────────────────────┐
│           Switching Techniques               │
├──────────────┬───────────────┬───────────────┤
│   Circuit    │    Packet     │    Message    │
│  Switching   │   Switching   │   Switching   │
└──────────────┴───────────────┴───────────────┘
```

---

## 2. Circuit Switching

### 2.1 Concept

A **dedicated end-to-end physical path** is established between sender and receiver **before** any communication begins. All resources (bandwidth, buffers) along that path are **reserved** for the duration of the connection.

```
Phase 1 — SETUP:
Source ────→ [Reserve bandwidth] ────→ Destination
             (Path locked in)

Phase 2 — DATA TRANSFER:
Source ════════════════════════════ Destination
        (Exclusive dedicated path)

Phase 3 — TEARDOWN:
Source ────→ [Release resources] ────→ Destination
```

### 2.2 Analogy

> Like a **railway track reservation**: you book an entire track from city A to city B. No other train can use that track while yours is running — even if your train is stopped at a station.

### 2.3 How It Works Technically

```
Example: Voice call from Mumbai to Delhi via 3 intermediate switches

                 SW1         SW2
Mumbai ───── [Switch 1] ─── [Switch 2] ─── Delhi

1. Mumbai phone sends SETUP signal through network
2. Each switch reserves a time slot (TDM channel) on each link:
   Link 1: Mumbai → SW1   → reserves slot 3
   Link 2: SW1   → SW2   → reserves slot 7
   Link 3: SW2   → Delhi  → reserves slot 2
3. SETUP ACK reaches Mumbai: "Your path is ready"
4. Call begins: voice data flows in real-time, no per-packet routing decisions
5. When call ends: TEARDOWN signal frees all reserved slots
```

### 2.4 Multiplexing in Circuit Switching

To share physical links among multiple circuits:

```
FDM — Frequency Division Multiplexing:
  Link divided into frequency bands; each circuit gets one band
  ┌──── f1 ────┬──── f2 ────┬──── f3 ────┬──── f4 ────┐
  │  Circuit A │  Circuit B │  Circuit C │  Circuit D │
  └────────────┴────────────┴────────────┴────────────┘

TDM — Time Division Multiplexing:
  Link divided into time slots; circuits take turns
  ┌──A──┬──B──┬──C──┬──D──┬──A──┬──B──┬──C──┬──D──┐ → time
  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

### 2.5 Advantages & Disadvantages

| ✅ Advantages | ❌ Disadvantages |
|--------------|-----------------|
| **Guaranteed bandwidth** — no competition | **Wasted capacity** — reserved even when silent |
| **Predictable, constant delay** | **Setup delay** — must wait before data flows |
| **No overhead per data unit** | **Inflexible** — if a node fails, call drops |
| **Ideal for real-time voice** | **Expensive** — dedicating resources is costly |
| Simple data transfer (no addressing) | **Doesn't scale** well for bursty data traffic |

### 2.6 Real-World Examples

- **PSTN** — Public Switched Telephone Network (traditional phone calls)
- **ISDN** — Integrated Services Digital Network
- **Early cellular (2G voice calls)**

---

## 3. Packet Switching ⭐ IMPORTANT

### 3.1 Concept

The message is broken into small, fixed-or-variable chunks called **packets**. Each packet is transmitted **independently** — carrying its own header with addressing information — and may take **different paths** to the destination. They are **reassembled** at the destination.

```
Message: "HELLO INTERNET"

Sender splits into packets:
  Packet 1: [Hdr: Seq=1, Dst=B] | "HELLO "
  Packet 2: [Hdr: Seq=2, Dst=B] | "INTERN"
  Packet 3: [Hdr: Seq=3, Dst=B] | "ET"

Each packet routes independently:
  Pkt 1 ──→ Router A ──→ Router C ──→ B
  Pkt 2 ──→ Router A ──→ Router D ──→ B   ← different path!
  Pkt 3 ──→ Router B (direct)

Destination B reassembles: "HELLO INTERNET" ✅
```

### 3.2 Store-and-Forward

At each router, the **entire packet** is received before it is forwarded:

```
Router receives packet:
  1. STORE  → Buffer the entire packet
  2. CHECK  → Verify packet integrity (FCS check)
  3. DECIDE → Look up routing table for next hop
  4. FORWARD → Send packet out appropriate interface

This is "Store-and-Forward" switching
```

**Transmission delay at each hop:**
$$\text{Delay per hop} = \frac{L}{R}$$
where $L$ = packet size in bits, $R$ = link rate in bps.

**Total end-to-end delay (no queuing, N links):**
$$\text{Total delay} = N \times \frac{L}{R}$$

**Example:**
```
3 links, 1000-bit packets, 1 Mbps each:
Total delay = 3 × (1000 / 1,000,000) = 3 ms
```

### 3.3 Two Modes of Packet Switching

#### A. Datagram (Connectionless)
- **No setup phase** — packets sent immediately
- Each packet carries **full source + destination address**
- Each router makes an **independent forwarding decision** per packet
- Packets may take **different routes** → arrive **out of order**
- Destination **reorders** packets
- **More resilient** — if a router fails, packets reroute automatically

```
Source sends 3 packets to Destination:

Packet 1 → Router A → Router C → Destination  (via path A-C)
Packet 2 → Router A → Router B → Destination  (via path A-B, different!)
Packet 3 → Router A → Router C → Destination  (via path A-C)

Arrive at dest: Pkt1, Pkt3, Pkt2 (out of order!) → TCP reorders
```

**Example: IP (Internet Protocol)**

#### B. Virtual Circuit (Connection-Oriented)
- **Setup phase** establishes a **logical path** (virtual circuit) before data flows
- All packets follow the **same predetermined path**
- Packets carry a **short VC label** instead of full addresses
- Arrive **in order**
- **Resources NOT dedicated** (unlike circuit switching — key difference!)

```
Setup: Source → VC ID=5 established → Destination
Data: All packets labeled VC=5 follow same path, in order
Teardown: Release VC=5
```

**Examples: ATM (Asynchronous Transfer Mode), MPLS, Frame Relay**

| Feature | Datagram | Virtual Circuit |
|---------|----------|----------------|
| Setup required | ❌ No | ✅ Yes |
| Addresses per packet | Full src/dst | Short VC label |
| Path per packet | May differ | Same always |
| Order at dest | May be out of order | In order |
| Resource reservation | ❌ No | ❌ No (just a logical path) |
| Resilience | ✅ Automatic rerouting | ❌ Must re-establish VC |
| Example | **IP (Internet)** | ATM, MPLS |

### 3.4 Statistical Multiplexing

Packet switching uses **statistical multiplexing** — link capacity is shared dynamically based on demand:

```
Circuit Switching (TDM):
  A: ─ slot ─ ─ idle ─ ─ idle ─ ─ slot ─  (slot reserved even when idle!)
  B: ─ idle ─ ─ slot ─ ─ idle ─ ─ idle ─
  C: ─ idle ─ ─ idle ─ ─ slot ─ ─ idle ─

Packet Switching (Statistical):
  A: ─ PKTPKT ─────────── PKT ─────────   (only uses link when it has data)
  B: ──────── PKT ──────────── PKT ────
  C: ─────────────── PKTPKT ─────────
  Link: AABCBCAA... (whoever has data, uses the link — efficient!)
```

> Internet traffic is inherently **bursty** — you download a page, pause, read, download again. Packet switching is perfectly suited for bursty traffic.

### 3.5 Advantages & Disadvantages

| ✅ Advantages | ❌ Disadvantages |
|--------------|-----------------|
| **Efficient** — no wasted reserved bandwidth | **Variable delay** — queuing causes jitter |
| **Fault tolerant** — alternate routes used | **Out-of-order delivery** (datagram) |
| **No setup delay** — send immediately | **Overhead** — every packet carries headers |
| **Scales to internet size** | **Packet loss** if buffers overflow |
| **Handles bursty traffic** perfectly | Not ideal for strict real-time (though DSCP/QoS help) |

### 3.6 Real-World Example: How IP Packet Switching Works

```
You visit www.google.com:
  1. Your browser creates an HTTP request (data = ~500 bytes)
  2. TCP splits into segments, IP wraps into packets
  3. Packets leave your router, hop through ISP routers
  4. Each router consults its routing table per packet
  5. Google receives packets (possibly out of order)
  6. TCP reassembles in correct order
  7. Your browser renders the page ✅
```

---

## 4. Message Switching

### 4.1 Concept

The **entire message** (no splitting) is sent to an intermediate node, which **stores the complete message** and then **forwards it** when the outgoing link is available. Also called **"store-and-forward"** (though this term is also used for packet switching at the router level).

```
Source → [Full Message stored at Node 1]
                    ↓ (when link is free)
         Node 1 → [Full Message stored at Node 2]
                              ↓ (when link is free)
                   Node 2 → Destination ✅
```

### 4.2 Analogy

> Like **snail mail (postal system)**: you hand your letter to the post office (Node 1). They hold it, sort it, and when a mail truck goes toward the destination, they forward it. The entire letter travels as one piece.

### 4.3 Advantages & Disadvantages

| ✅ Advantages | ❌ Disadvantages |
|--------------|-----------------|
| No dedicated path needed | **Huge storage required** at each node |
| Works when links are busy (queue it) | **High delay** — large messages block links |
| Messages can be prioritized | **Not real-time** suitable |
| Error checking at each hop | Inefficient for time-sensitive data |

### 4.4 Real-World Examples

- **Email** (SMTP is store-and-forward — mail server holds and delivers)
- **Telegraph/telex systems** (historical)
- **Store-and-forward fax**

---

## 5. Comparison: All Three Switching Types

| Feature | Circuit Switching | Packet Switching | Message Switching |
|---------|:-----------------:|:----------------:|:-----------------:|
| **Path** | Dedicated | Dynamic (per packet) | Dynamic (per message) |
| **Setup required** | ✅ Yes | ❌ No (datagram) | ❌ No |
| **Data stored at node** | ❌ No | Briefly (one packet) | ✅ Full message |
| **Bandwidth** | Wasted when idle | Efficient (shared) | Efficient |
| **Delay (after setup)** | Very low, constant | Variable | High |
| **Order preserved** | ✅ Always | ❌ Not always | ❌ Not always |
| **Real-time suitable** | ✅ Best | ✅ Yes (with QoS) | ❌ No |
| **Fault tolerance** | ❌ Poor | ✅ Excellent | ✅ Good |
| **Overhead** | Low (no headers) | Per-packet headers | Per-message |
| **Scalability** | ❌ Limited | ✅ Internet-scale | ❌ Limited |
| **Best for** | Voice, PSTN | **Internet, data** | Email, messaging |
| **Example** | Phone (PSTN) | **IP Networks** | SMTP, Telegram |

---

## 6. Key Diagrams

### Circuit vs Packet — Bandwidth Utilization
```
Circuit Switching:
Time: ──A─────────────────────────B──────────────────────────────
      [──────── Reserved for User X ────────][────── User Y ─────]
                ↑ Wasted if no data!

Packet Switching (Statistical Multiplexing):
Time: ──X──Y──Y──X──Z──X──Y──Z──Z──X──Y──X──Y──Z──X──Y──
      (whoever has data uses the link — very efficient!)
```

### Packet Switching — Store and Forward

```
Router:
           Packet arrives    Check    Route lookup    Forward
  Input ──→[===buffer===] ──→ FCS ──→ Routing table ──→ Output
              ↑ stored                                    ↑ sent
              (must receive fully before forwarding)
```

---

## 7. Interview Questions

**Q1: What is the main difference between circuit switching and packet switching?**
> Circuit switching establishes a dedicated path before communication, reserving bandwidth throughout — guaranteed but wasteful. Packet switching breaks data into packets that route independently; bandwidth is shared efficiently but delivery has variable delay.

**Q2: Why is packet switching preferred for the internet?**
> Internet traffic is bursty — users don't continuously send at full rate. Packet switching uses statistical multiplexing, sharing links efficiently among many users. Circuit switching would waste bandwidth during the gaps, and dedicating circuits to every internet user would be impossible at scale.

**Q3: What is the difference between datagram and virtual circuit packet switching?**
> Datagram: each packet carries full addresses, routed independently, may take different paths, arrive out of order (used by IP). Virtual circuit: a logical path is set up first, packets follow the same path with short labels, arrive in order (used by ATM, MPLS).

**Q4: What is store-and-forward in packet switching?**
> Each router receives the complete packet, verifies its integrity, consults the routing table, and then forwards it. This adds per-hop transmission delay but allows error checking at every router.

**Q5: What is statistical multiplexing?**
> Multiple data streams share a link based on statistical demand — when one user is idle, others use the full link. Unlike TDM/FDM (which pre-allocate fixed slots), statistical multiplexing dynamically allocates capacity, greatly improving link utilization for bursty traffic.

**Q6: Why is message switching not suitable for real-time applications?**
> The entire message is stored at each intermediate node before forwarding. Large messages can occupy a node's link for a long time, blocking other traffic and introducing unpredictable, potentially very high delays — incompatible with real-time voice or video requirements.

---

*Next: [02 — Network Delays →](./02_Network_Delays.md)*
