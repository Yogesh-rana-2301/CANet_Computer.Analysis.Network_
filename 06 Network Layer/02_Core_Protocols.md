# Core Protocols — ICMP & ARP

> ⭐ **ARP is VERY IMPORTANT** — frequently asked in interviews at all levels!

---

## 1. ARP — Address Resolution Protocol ⭐

### 1.1 The Problem ARP Solves

The Network Layer thinks in **IP addresses**. The Data Link Layer thinks in **MAC addresses**. When a packet needs to be delivered on a local network, the sender knows the destination **IP** (from the routing table) but needs the destination **MAC** to build the frame.

**ARP bridges this gap**: It translates **IP addresses → MAC addresses**.

```
You want to send to: 192.168.1.50
You know:            IP = 192.168.1.50
You DON'T know:      MAC = ???
                       ↓
                   Use ARP!
```

### 1.2 ARP Operation — Step by Step

```
Network: 192.168.1.0/24

Host A (192.168.1.1, MAC: AA:AA:AA:AA:AA:AA)
Host B (192.168.1.50, MAC: BB:BB:BB:BB:BB:BB)
Host C (192.168.1.99, MAC: CC:CC:CC:CC:CC:CC)

Scenario: A wants to send a packet to B
```

#### Step 1: Check ARP Cache
```
Host A checks its ARP table:
  IP              MAC              TTL
  ─────────────────────────────────────
  (192.168.1.50 not found!)
→ Must perform ARP resolution
```

#### Step 2: ARP Request (Broadcast)
```
Host A sends an ARP Request:
  ┌────────────────────────────────────────────────┐
  │ Ethernet Frame:                                │
  │   Dest MAC:    FF:FF:FF:FF:FF:FF  ← BROADCAST │
  │   Src  MAC:    AA:AA:AA:AA:AA:AA               │
  │                                                │
  │ ARP Payload:                                   │
  │   "Who has 192.168.1.50? Tell 192.168.1.1"    │
  │   Sender IP:  192.168.1.1                      │
  │   Sender MAC: AA:AA:AA:AA:AA:AA                │
  │   Target IP:  192.168.1.50                     │
  │   Target MAC: 00:00:00:00:00:00  ← Unknown    │
  └────────────────────────────────────────────────┘

All devices on the LAN receive this broadcast!
```

#### Step 3: ARP Reply (Unicast)
```
Host B recognizes its own IP (192.168.1.50) → sends ARP Reply:
  ┌────────────────────────────────────────────────┐
  │ Ethernet Frame:                                │
  │   Dest MAC:  AA:AA:AA:AA:AA:AA  ← UNICAST     │
  │   Src  MAC:  BB:BB:BB:BB:BB:BB                 │
  │                                                │
  │ ARP Payload:                                   │
  │   "192.168.1.50 is at BB:BB:BB:BB:BB:BB"      │
  │   Sender IP:  192.168.1.50                     │
  │   Sender MAC: BB:BB:BB:BB:BB:BB                │
  └────────────────────────────────────────────────┘
```

#### Step 4: Cache the Result
```
Host A updates its ARP cache:
  IP              MAC                  TTL
  ──────────────────────────────────────────────
  192.168.1.50    BB:BB:BB:BB:BB:BB    120 sec
```

#### Step 5: Send the Packet
```
Host A can now build the frame:
  Dest MAC: BB:BB:BB:BB:BB:BB
  Src MAC:  AA:AA:AA:AA:AA:AA
  Dest IP:  192.168.1.50
  Src IP:   192.168.1.1
```

### 1.3 ARP Cache

ARP results are **cached** to avoid sending a broadcast for every packet:

```
$ arp -a   (view ARP table on your computer)

Interface: 192.168.1.1
  Internet Address    Physical Address    Type
  192.168.1.50        BB-BB-BB-BB-BB-BB  dynamic
  192.168.1.1         AA-AA-AA-AA-AA-AA  static
```

- **Dynamic entries**: Learned via ARP, expire after ~20 min (OS-dependent)
- **Static entries**: Manually configured, permanent
- When TTL expires → entry removed → next communication triggers a new ARP request

### 1.4 ARP Packet Format

```
 Hardware Type  (2B)  — 1 = Ethernet
 Protocol Type  (2B)  — 0x0800 = IPv4
 HW Addr Length (1B)  — 6 (MAC = 6 bytes)
 Proto Addr Len (1B)  — 4 (IPv4 = 4 bytes)
 Operation      (2B)  — 1=Request, 2=Reply
 Sender MAC     (6B)
 Sender IP      (4B)
 Target MAC     (6B)  — all zeros in request
 Target IP      (4B)
```

### 1.5 ARP for Different Destinations

#### Same Subnet
```
A (192.168.1.1) → B (192.168.1.50) [same /24]
A ARPs for B's MAC directly
Frame: Dest MAC = B's MAC
```

#### Different Subnet (via Router)
```
A (192.168.1.1) → C (10.0.0.5) [different network]
A knows: destination not on local network → send to default gateway!
A ARPs for the ROUTER's MAC (not C's MAC)
Frame: Dest MAC = Router's MAC, Dest IP = 10.0.0.5 (C's IP)
```

> **Key rule**: ARP is always for the **next hop MAC**, not the final destination MAC.

### 1.6 Gratuitous ARP

A device sends an **ARP request for its own IP** at startup:
- Announces itself to the network
- Updates other devices' ARP caches
- Detects IP conflicts (if someone replies, there's a duplicate!)

```
Host A powers up with IP 192.168.1.10:
  Sends ARP: "Who has 192.168.1.10? Tell 192.168.1.10"
  ↓
  If anyone replies → IP CONFLICT! ⚠️
  If nobody replies → All clear, A is the only owner
```

### 1.7 ARP Spoofing (Security Attack)

An attacker sends **fake ARP replies** to poison ARP caches:

```
Attacker sends to A: "192.168.1.1 (router) is at ATTACKER_MAC"
Attacker sends to Router: "192.168.1.5 (victim) is at ATTACKER_MAC"

Now:
  A → Router traffic goes to Attacker → Man-in-the-Middle! ⚠️
```

**Countermeasure**: Dynamic ARP Inspection (DAI) on switches, static ARP entries.

### 1.8 Proxy ARP

A router answers ARP requests **on behalf of another device** on a different subnet. Allows devices without a configured default gateway to still communicate.

### 1.9 RARP — Reverse ARP

**RARP** does the opposite of ARP: given a **MAC address**, find the **IP address**. Used by diskless workstations at boot. Now replaced by **DHCP**.

```
ARP:  IP → MAC  (most common)
RARP: MAC → IP  (legacy, replaced by DHCP)
```

---

## 2. ICMP — Internet Control Message Protocol

### 2.1 What is ICMP?

ICMP is a **network-layer protocol** used for **error reporting and diagnostics**. It doesn't carry user data — it carries **control messages** between network devices.

```
ICMP is encapsulated in an IP packet:
  IP Header [Protocol = 1 (ICMP)] + ICMP Message
```

### 2.2 ICMP Message Types

ICMP messages have a **Type** and **Code** field:

| Type | Name | Common Use |
|------|------|------------|
| **0** | Echo Reply | Ping response |
| **3** | Destination Unreachable | Host/port unreachable |
| **4** | Source Quench | Congestion control (deprecated) |
| **5** | Redirect | Better route available |
| **8** | Echo Request | Ping request |
| **9** | Router Advertisement | Router discovery |
| **11** | Time Exceeded | TTL expired (traceroute) |
| **12** | Parameter Problem | Bad IP header |

### 2.3 ICMP Type 3 — Destination Unreachable Codes

| Code | Meaning |
|------|---------|
| 0 | Network unreachable |
| 1 | Host unreachable |
| 2 | Protocol unreachable |
| 3 | **Port unreachable** (common — sent when UDP port not open) |
| 4 | Fragmentation needed but DF bit set |
| 5 | Source route failed |

### 2.4 Ping — How It Works

`ping` uses **ICMP Echo Request (Type 8)** and **Echo Reply (Type 0)**:

```
Step 1: A sends ICMP Echo Request to B
  ┌─────────────────────────────────────┐
  │ IP: Src=192.168.1.1 Dst=192.168.1.50│
  │ ICMP Type=8 (Echo Request)          │
  │ Identifier: 1234                    │
  │ Sequence: 1                         │
  │ Data: timestamp + padding           │
  └─────────────────────────────────────┘

Step 2: B receives, sends ICMP Echo Reply
  ┌─────────────────────────────────────┐
  │ IP: Src=192.168.1.50 Dst=192.168.1.1│
  │ ICMP Type=0 (Echo Reply)            │
  │ Identifier: 1234                    │
  │ Sequence: 1                         │
  └─────────────────────────────────────┘

Step 3: A measures RTT = time between request and reply
Output: "64 bytes from 192.168.1.50: icmp_seq=1 ttl=64 time=0.4ms"
```

### 2.5 Traceroute — How It Works

`traceroute` (or `tracert`) reveals the **path** packets take to a destination by exploiting the **TTL field**:

```
TTL (Time To Live) is decremented by 1 at each router.
When TTL reaches 0 → router drops packet and sends ICMP Time Exceeded (Type 11) back.

Traceroute sends packets with incrementing TTL:

Probe 1: TTL=1
  A → Router1 (TTL becomes 0) → Router1 sends "Time Exceeded" back to A
  A records: "First hop is Router1, RTT=X ms"

Probe 2: TTL=2
  A → Router1 (TTL=1) → Router2 (TTL=0) → Router2 sends "Time Exceeded"
  A records: "Second hop is Router2, RTT=Y ms"

Probe 3: TTL=3
  A → R1 → R2 → Destination (destination sends Echo Reply or Port Unreachable)
  A records: "Reached destination!"
```

```
$ traceroute google.com
 1  192.168.1.1      1.2 ms    ← Home router
 2  10.20.30.1       5.4 ms    ← ISP gateway
 3  72.14.204.1      8.1 ms    ← ISP backbone
 4  142.250.68.46    9.2 ms    ← Google edge
```

### 2.6 ICMP and Security

- **ICMP flood** (ping flood): attacker sends massive ping requests — DoS attack
- **Ping of Death**: oversized ping packet (historical vulnerability)
- **ICMP redirect attack**: attacker sends fake ICMP redirect to reroute traffic
- Many firewalls **block ICMP** — though this breaks `ping` and `traceroute`

### 2.7 ICMPv6

IPv6 uses **ICMPv6** (far more important than ICMPv4):
- Replaces ARP (using **Neighbor Discovery Protocol — NDP**)
- Router discovery/advertisement
- Path MTU discovery
- Multicast listener discovery

```
ICMPv6 Type 135 = Neighbor Solicitation  (like ARP Request)
ICMPv6 Type 136 = Neighbor Advertisement (like ARP Reply)
```

---

## 3. DHCP — Dynamic Host Configuration Protocol (Bonus)

> Not in your list, but often asked alongside ARP!

DHCP automatically assigns IP, subnet mask, default gateway, and DNS to clients.

**DORA Process:**
```
Client              DHCP Server
  │─── Discover ──────────→│  (Broadcast: "I need an IP!")
  │←── Offer ─────────────│  (Server offers: "Take 192.168.1.50/24")
  │─── Request ───────────→│  (Client: "I'll take it!")
  │←── Acknowledge ────────│  (Server: "It's yours for X seconds")
```

---

## 4. Comparison: ARP vs ICMP vs DHCP

| Protocol | Purpose | Layer | Direction |
|---------|---------|-------|-----------|
| **ARP** | IP → MAC mapping | L2/L3 boundary | Request/Reply |
| **RARP** | MAC → IP mapping | L2/L3 boundary | Request/Reply |
| **ICMP** | Error reporting, diagnostics | L3 | Informational |
| **DHCP** | Auto IP configuration | L7 (uses UDP) | DORA process |

---

## 5. Interview Questions

**Q1: What is ARP and why is it needed?**
> ARP (Address Resolution Protocol) maps IP addresses to MAC addresses. It's needed because routers use IP for routing (Layer 3), but actual frame delivery on a LAN requires MAC addresses (Layer 2). Without ARP, a device knowing only the destination IP cannot build a valid Layer 2 frame.

**Q2: Is the ARP request unicast or broadcast? What about the reply?**
> ARP Request is a **broadcast** (FF:FF:FF:FF:FF:FF) so all LAN devices receive it. ARP Reply is a **unicast** sent directly back to the requester.

**Q3: What is ARP cache and why does it have a TTL?**
> ARP cache stores recent IP→MAC mappings to avoid repeated ARP broadcasts. TTL prevents stale entries — if a device's MAC changes (NIC replaced), old cached entries would cause delivery failures.

**Q4: What is Gratuitous ARP?**
> A device ARPs for its own IP address at startup. Used to: announce its presence, update peers' caches, and detect IP address conflicts (if anyone replies, there's a duplicate).

**Q5: What does ICMP Type 11 mean?**
> Time Exceeded — the TTL of a packet reached 0 and was dropped by a router. This is exactly what `traceroute` exploits to map the path to a destination.

**Q6: What is the difference between ping and traceroute?**
> `ping` checks reachability and round-trip time using ICMP Echo Request/Reply. `traceroute` reveals the full path by sending packets with incrementally increasing TTL values (1, 2, 3...) and recording ICMP Time Exceeded messages from each router along the way.

**Q7: What happens in ARP when the destination is on a different network?**
> The sender ARPs for the **default gateway's MAC** (not the destination's), because Layer 2 delivery is only hop-by-hop. The frame is sent to the router (gateway), which then handles routing to the final destination.

**Q8: What is ARP Spoofing?**
> An attacker sends fake ARP replies to poison ARP caches, making devices send traffic to the attacker's MAC instead of the legitimate destination — enabling a Man-in-the-Middle attack.

---

*Next: [03 — Routing →](./03_Routing.md)*
