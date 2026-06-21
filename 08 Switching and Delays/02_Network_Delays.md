# ⏱️ Network Delays ⭐

> Understanding the four sources of delay is fundamental to network performance analysis. This is a very common interview and exam topic!

---

## 1. The Four Types of Network Delay

When a packet travels from source to destination, it experiences delay at **every node (router/switch)** and on **every link**. There are exactly four sources:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Total Node Delay                             │
│                                                                 │
│  d_total = d_proc + d_queue + d_trans + d_prop                 │
│              ↑         ↑         ↑         ↑                   │
│           Processing  Queuing  Transmission Propagation        │
└─────────────────────────────────────────────────────────────────┘
```

**Visual journey of a packet:**

```
[Sender] ──────────────────────────────────────── [Receiver]
            ↓ At each router/switch:
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Packet   d_proc    d_queue     d_trans         d_prop  │
│  arrives ──────→ [Routing] → [Wait in] → [Put bits] ──→ │
│           (check    lookup     queue      on wire)       │
│           errors)                                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Transmission Delay

### 2.1 Definition

**Transmission delay** is the time required to **push all the bits of a packet onto the wire (link)**. It is the time from when the first bit is sent until the last bit is sent.

> Think of it as: "How long does it take to *load* the packet onto the link?"

### 2.2 Formula

$$d_{trans} = \frac{L}{R}$$

where:
- $L$ = **packet length** in bits
- $R$ = **link transmission rate** (bandwidth) in bits per second (bps)

### 2.3 Examples

```
Example 1:
  Packet size: L = 1,000 bits
  Link speed: R = 1 Mbps = 1,000,000 bps
  d_trans = 1,000 / 1,000,000 = 0.001 sec = 1 ms

Example 2:
  Packet size: L = 1,500 bytes = 12,000 bits (×8)
  Link speed: R = 100 Mbps = 100,000,000 bps
  d_trans = 12,000 / 100,000,000 = 0.00012 sec = 0.12 ms

Example 3:
  Packet size: L = 1,000 bits
  Link speed: R = 1 Gbps = 1,000,000,000 bps
  d_trans = 1,000 / 1,000,000,000 = 0.000001 sec = 1 µs (microsecond!)
```

### 2.4 Key Insight

- Increasing bandwidth (**R**) → transmission delay ↓
- Smaller packets (**L**) → transmission delay ↓
- Transmission delay has **nothing to do with distance** — it's purely about bandwidth and packet size

```
High bandwidth: ████████ → (all bits pushed quickly)
Low bandwidth:  █        (bits trickle onto the link slowly)
                ↑
            Same packet, but takes much longer to send!
```

---

## 3. Propagation Delay

### 3.1 Definition

**Propagation delay** is the time it takes for the **signal (electromagnetic wave / light pulse) to travel from sender to receiver** through the physical medium, after all bits are pushed onto the link.

> Think of it as: "How long does the signal take to *travel* through the wire?"

### 3.2 Formula

$$d_{prop} = \frac{d}{s}$$

where:
- $d$ = **distance** of the link in meters
- $s$ = **propagation speed** of the medium in m/s

### 3.3 Propagation Speeds

| Medium | Speed | As fraction of speed of light |
|--------|-------|-------------------------------|
| **Vacuum (theoretical)** | $3 \times 10^8$ m/s | 1.0c |
| **Fiber optic** | $\approx 2 \times 10^8$ m/s | ~0.67c |
| **Copper wire (Ethernet)** | $\approx 2 \times 10^8$ m/s | ~0.64c |
| **Wireless (radio)** | $\approx 3 \times 10^8$ m/s | ~1.0c |

### 3.4 Examples

```
Example 1: Ethernet cable across a room
  Distance: d = 10 m
  Speed: s = 2×10⁸ m/s
  d_prop = 10 / (2×10⁸) = 5×10⁻⁸ sec = 50 nanoseconds (negligible!)

Example 2: Fiber optic coast-to-coast (USA: ~4,000 km)
  Distance: d = 4,000,000 m
  Speed: s = 2×10⁸ m/s
  d_prop = 4,000,000 / (2×10⁸) = 0.02 sec = 20 ms

Example 3: Satellite link (geostationary orbit, 35,786 km)
  Distance: d = 35,786,000 m (one way)
  Speed: s = 3×10⁸ m/s
  d_prop = 35,786,000 / (3×10⁸) ≈ 0.119 sec ≈ 119 ms ONE WAY
  Round trip: ~238 ms ← Why satellite internet feels laggy!
```

### 3.5 Key Insight

- Propagation delay depends **only on distance and medium** — not on bandwidth or packet size
- You can have a 100 Gbps fiber link across a continent, but the propagation delay is fixed at ~20ms — you can't speed it up by increasing bandwidth
- This is why **geographically closer servers** are faster (CDNs, edge computing)

```
Bandwidth analogy:
  Highway width = Bandwidth (R)
  Highway length = Distance (d)
  Cars on highway = bits

  Wider highway → more cars fit (high bandwidth → low transmission delay)
  Longer highway → cars take longer to arrive (distance → high propagation delay)

  COMPLETELY independent effects!
```

---

## 4. Queuing Delay

### 4.1 Definition

**Queuing delay** is the time a packet spends **waiting in the router's buffer/queue** before it can be transmitted, because the outgoing link is busy serving other packets.

> Think of it as: "How long does the packet wait in line at the router?"

### 4.2 When Does Queuing Delay Occur?

```
Packets arrive at router faster than they can be sent out:

Input rate (a):     ████████████████████████  → high arrival rate
Output link (R):    ────────────────────────  → fixed capacity

Buffer fills up:
  [Pkt4][Pkt3][Pkt2][Pkt1] → Link
   ↑ Pkt4 waits longest (queuing delay)
```

### 4.3 Traffic Intensity

The key metric is **traffic intensity** (or link utilization):

$$\text{Traffic Intensity} = \frac{L \cdot a}{R}$$

where:
- $L$ = packet size in bits
- $a$ = average packet arrival rate (packets/sec)
- $R$ = link capacity (bits/sec)
- $L \cdot a$ = average bits arriving per second

| Traffic Intensity | Queuing Behavior |
|------------------|------------------|
| ≈ 0 | Very small queuing delay |
| → 1 | Queuing delay grows rapidly |
| ≥ 1 | Queue grows infinitely → **packet loss!** |

```
Queuing Delay vs Traffic Intensity:

Delay
  ∞ │                                    ╱
    │                                   ╱
    │                                  ╱
    │                                 ╱
    │                            ╱────
    │                       ╱────
    │               ╱───────
    │──────────────
    └──────────────────────────────────→ Traffic Intensity (La/R)
    0                                 1
```

### 4.4 Queuing Delay Characteristics

- **Most variable** of all four delays — can range from 0 to ∞
- Depends on **traffic patterns** (bursty vs. uniform)
- **Statistical in nature** — impossible to give a simple formula
- When traffic intensity → 1: queuing delay → very large
- When traffic intensity > 1: **packets are dropped** (buffer overflow)

### 4.5 Packet Loss

When the router's buffer is **full** and a new packet arrives:
```
Buffer: [P4][P3][P2][P1] ← FULL
New packet arrives: [P5]

Options:
  1. DROP P5 (tail-drop — most common)
  2. DROP P4 (head-drop)
  3. Random Early Detection (RED) — drop randomly before full
```

Dropped packets → TCP detects loss → TCP retransmits → Higher latency

---

## 5. Processing Delay

### 5.1 Definition

**Processing delay** is the time a router takes to **examine the packet header, check for bit errors, and determine the output link** (routing table lookup).

> Think of it as: "How long does the router spend thinking about where to send the packet?"

### 5.2 What Processing Involves

```
Packet arrives at router:
  1. Check FCS (Frame Check Sequence) — bit error detection
  2. Read destination IP address
  3. Routing table lookup → determine next hop
  4. Update TTL (decrement by 1)
  5. Recompute IP header checksum
  6. Place packet in appropriate output queue
```

### 5.3 Characteristics

- Typically on the order of **microseconds** on modern routers
- Depends on **router hardware** — custom ASICs are much faster than software
- **Fixed/bounded** — doesn't grow with traffic (unlike queuing delay)
- Can be significant in **software routers** or when processing **complex rules** (firewalls, NAT)

### 5.4 How to Minimize

- **Hardware routing** (ASIC chips) instead of software
- **IP Longest Prefix Match** done in TCAM (Ternary Content Addressable Memory) — lookups in O(1)
- Caching frequently used routing entries

---

## 6. Total End-to-End Delay

### 6.1 Formula

For a path with **N links** (N−1 routers + source + destination):

$$d_{end-to-end} = \sum_{i=1}^{N} \left( d_{proc_i} + d_{queue_i} + d_{trans_i} + d_{prop_i} \right)$$

**Simplified** (ignoring processing and queuing, which are often small/variable):

$$d_{end-to-end} \approx N \cdot \frac{L}{R} + \frac{d_{total}}{s}$$

### 6.2 Full Worked Example

**Setup:**
```
Source ──(Link 1)── Router A ──(Link 2)── Router B ──(Link 3)── Destination

Links: 
  All links: 1 Mbps bandwidth
  Link 1 length: 1,000 km
  Link 2 length: 500 km
  Link 3 length: 2,000 km

Packet:
  Size: 8,000 bits (1,000 bytes)
  Propagation speed: 2×10⁸ m/s
  Processing delay per router: 1 ms
  Queuing delay per router: 2 ms (assume low traffic)
```

**Calculate each delay:**

```
Transmission delay per link:
  d_trans = L/R = 8,000 / 1,000,000 = 8 ms
  Total trans (3 links): 3 × 8 ms = 24 ms

Propagation delay:
  Link 1: 1,000,000 m / (2×10⁸) = 5 ms
  Link 2:   500,000 m / (2×10⁸) = 2.5 ms
  Link 3: 2,000,000 m / (2×10⁸) = 10 ms
  Total prop: 5 + 2.5 + 10 = 17.5 ms

Processing delay (2 routers):
  Total proc: 2 × 1 ms = 2 ms

Queuing delay (2 routers):
  Total queue: 2 × 2 ms = 4 ms

TOTAL END-TO-END DELAY:
  = 24 + 17.5 + 2 + 4 = 47.5 ms
```

### 6.3 Pipelining: Multiple Packets

When sending multiple packets, **pipelining** occurs — subsequent packets can be in transit while earlier ones are still traveling:

```
3 packets, 2 links, L=1000 bits, R=1 Mbps, prop=5ms each

Without pipelining (wrong model):
  Time = 3 packets × 2 links × 1ms + 2 × 5ms prop = 16 ms

With pipelining (correct model):
  Pkt1:  [──trans──][prop][──trans──][prop]   → arrives at T=12ms
  Pkt2:       [──trans──][prop][──trans──][prop] → T=13ms
  Pkt3:            [──trans──][prop][──trans──][prop] → T=14ms
                                                          ↑ only 2ms gap!
  All 3 packets arrive by T=14ms (not 3×12ms=36ms)
```

---

## 7. Delay-Bandwidth Product

The **delay-bandwidth product** tells you how many bits can be "in flight" on a link at any given time:

$$\text{Delay-Bandwidth Product} = R \times d_{prop}$$

```
Example: 100 Mbps fiber, 5ms propagation delay

DBP = 100×10⁶ × 0.005 = 500,000 bits = 500 Kbits ≈ 62.5 KB

This means the link can hold 500,000 bits in transit simultaneously.
Like a "pipe" — wider (bandwidth) × longer (delay) = capacity of the pipe.
```

---

## 8. Summary Comparison Table

| Delay Type | Formula | Controlled by | Typical Range | Where it occurs |
|-----------|---------|--------------|--------------|----------------|
| **Processing** | Fixed | Router CPU/hardware | µs | At each router |
| **Queuing** | Statistical | Traffic load | 0 – ∞ ms | At each router buffer |
| **Transmission** | L / R | Bandwidth, packet size | µs – ms | At each link (sending) |
| **Propagation** | d / s | Distance, medium | ns – 250ms | Along each link (traveling) |

---

## 9. Interview Questions

**Q1: What are the four types of network delay?**
> Transmission delay (L/R — time to push bits onto the link), Propagation delay (d/s — time for signal to travel the link), Queuing delay (waiting in router buffer), Processing delay (router header inspection and routing lookup). Total = sum of all four at each hop.

**Q2: What is the formula for transmission delay and what factors affect it?**
> d_trans = L/R, where L = packet size in bits, R = link bandwidth in bps. A larger packet or lower bandwidth increases transmission delay. Distance has no effect on transmission delay.

**Q3: What is the difference between transmission delay and propagation delay?**
> Transmission delay is about how fast bits are pushed onto the wire (depends on bandwidth and packet size). Propagation delay is about how fast the signal physically travels through the medium (depends on distance and speed of light in the medium). They are completely independent.

**Q4: What is traffic intensity and why does it matter?**
> Traffic intensity = La/R, where La is the arrival rate of bits and R is link capacity. When traffic intensity approaches 1, queuing delay increases dramatically. When it exceeds 1, the queue grows without bound and packets are dropped.

**Q5: Why can satellite internet have high latency even with high bandwidth?**
> Satellite internet has very high propagation delay (~238ms round-trip for geostationary satellites at 36,000 km altitude). No amount of bandwidth increase can reduce propagation delay — it's fixed by the speed of light and distance.

**Q6: What happens when a router's buffer overflows?**
> Packets are dropped (packet loss). TCP detects this (missing ACKs or duplicate ACKs), reduces its sending rate, and retransmits the lost segment — adding significant latency and reducing throughput.

**Q7: A packet is 8000 bits long, link is 1 Mbps. What is the transmission delay?**
> d_trans = L/R = 8000 / 1,000,000 = 8 ms.

**Q8: What is the delay-bandwidth product?**
> DBP = R × d_prop — the number of bits that can be "in flight" in the link pipeline at once. It represents the link's capacity like a pipe: wider (more bandwidth) and longer (more propagation delay) = more bits in transit simultaneously.

---

*← Back to [Index](./README.md)*
