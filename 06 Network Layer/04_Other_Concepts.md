#  Other Concepts — Fragmentation, Tunneling & NAT

---

## 1. Fragmentation

### 1.1 What is Fragmentation?

When an IP packet is too large to travel through a network link, the router (in IPv4) or the source host (in IPv6) must **break it into smaller pieces** called **fragments**. These fragments travel independently and are **reassembled at the destination**.

```
Large Packet (4000 bytes)
─────────────────────────────────────────────
            │
            ▼ Link MTU = 1500 bytes
  ┌─────────────────┐
  │ Fragment 1      │  (1500 bytes)
  │ Fragment 2      │  (1500 bytes)
  │ Fragment 3      │  (1000 bytes)
  └─────────────────┘
            │
            ▼ Reassembled at destination
Large Packet (4000 bytes) 
```

### 1.2 MTU — Maximum Transmission Unit

**MTU** is the maximum payload size a link can carry in a single frame.

| Network Type | MTU |
|-------------|-----|
| **Ethernet** | **1500 bytes** (most common) |
| PPPoE | 1492 bytes |
| WiFi (802.11) | 2304 bytes |
| Token Ring | 4472 bytes |
| FDDI | 4352 bytes |
| Loopback | 65536 bytes |

> Standard Internet MTU = **1500 bytes** (Ethernet standard)

### 1.3 IPv4 Header Fields for Fragmentation

```
IPv4 Header:
  ┌────────────────┬─────────┬────────────────────────┐
  │ Identification │  Flags  │   Fragment Offset       │
  │    (16 bits)   │(3 bits) │     (13 bits)           │
  └────────────────┴─────────┴────────────────────────┘
```

| Field | Purpose | Details |
|-------|---------|---------|
| **Identification** | All fragments of same datagram share same ID | 16-bit value set by source |
| **Flags** | Control fragmentation | 3 bits |
| **Fragment Offset** | Position of this fragment in original | In units of 8 bytes |

#### Flags Field (3 bits):
```
Bit 0: Reserved (must be 0)
Bit 1: DF (Don't Fragment) — 0=may fragment, 1=must NOT fragment
Bit 2: MF (More Fragments) — 0=last fragment, 1=more fragments follow
```

### 1.4 How Fragmentation Works — Step by Step

**Given:**
- Original Datagram: 4000 bytes (IP payload)
- IP Header: 20 bytes
- Total size: 4020 bytes
- Link MTU: 1500 bytes
- Max data per fragment: 1500 − 20 = 1480 bytes

**Fragmentation calculation:**

```
Fragment 1:
  Data: bytes 0–1479       (1480 bytes)
  Offset: 0/8 = 0
  MF = 1 (more fragments)
  Total size: 1480 + 20 = 1500 bytes ✅

Fragment 2:
  Data: bytes 1480–2959    (1480 bytes)
  Offset: 1480/8 = 185
  MF = 1 (more fragments)
  Total size: 1480 + 20 = 1500 bytes ✅

Fragment 3:
  Data: bytes 2960–3999    (1040 bytes)
  Offset: 2960/8 = 370
  MF = 0 (LAST fragment)
  Total size: 1040 + 20 = 1060 bytes ✅
```

**Fragment Summary Table:**
| Fragment | Data Size | Offset | MF Bit | Total Size |
|---------|-----------|--------|--------|------------|
| 1 | 1480 | 0 | 1 | 1500 |
| 2 | 1480 | 185 | 1 | 1500 |
| 3 | 1040 | 370 | **0** | 1060 |

> **Key rule**: Fragment offset is always in **units of 8 bytes** (because the 13-bit field would otherwise not cover large datagrams).

### 1.5 Reassembly

- Only the **final destination** reassembles fragments — **intermediate routers do NOT reassemble**.
- The destination uses the **Identification field** to group fragments and the **Fragment Offset** to order them.
- A reassembly **timer** is started when the first fragment arrives; if all fragments don't arrive in time → all discarded.

```
Destination receives (possibly out of order):
  Fragment 3 (offset=370, MF=0) → knows total = 370×8+1040 = 3000+1040 = 4000 bytes needed
  Fragment 1 (offset=0, MF=1)
  Fragment 2 (offset=185, MF=1)

After all arrive:
  Reassembled: complete 4000-byte original datagram ✅
```

### 1.6 Fragmentation in IPv4 vs IPv6

| Aspect | IPv4 | IPv6 |
|--------|------|------|
| **Who fragments?** | Routers AND source | **Source host ONLY** |
| **DF bit** | Optional | No DF bit (always "don't fragment" for routers) |
| **How routers handle oversized?** | Fragment it | Send ICMP "Packet Too Big" back |
| **Fragment header** | Built into main header | Extension header |
| **Efficiency** | Fragmentation at routers (overhead) | Path MTU Discovery avoids fragmentation |

### 1.7 Path MTU Discovery (PMTUD)

IPv6 (and modern IPv4) use **Path MTU Discovery** to find the smallest MTU along the path and send packets that fit without fragmentation:

```
1. Source sends packet with DF=1 (Don't Fragment)
2. If a router can't forward it:
   → Sends ICMP "Fragmentation Needed" (IPv4) or "Packet Too Big" (IPv6)
   → Includes the link's MTU in the ICMP message
3. Source reduces packet size to that MTU
4. Retry with smaller packet
5. Eventually discovers the minimum MTU along the entire path
```

---

## 2. Tunneling

### 2.1 What is Tunneling?

Tunneling **encapsulates one protocol's packet inside another protocol's packet**, allowing it to travel through a network that doesn't natively support the original protocol.

```
Original Packet:  [IPv6 Header | Data]
After Tunneling:  [IPv4 Header | IPv6 Header | Data]
                   ↑ Outer header (IPv4 — understood by network)
                              ↑ Inner header (IPv6 — the real packet)
```

### 2.2 How Tunneling Works

```
Network: A ──IPv6─── [Tunnel Entry] ───IPv4 Internet─── [Tunnel Exit] ───IPv6─── B
                           │                                    │
               Encapsulates IPv6 in IPv4                Strips IPv4 header
               (IPv4 Header added)                      Delivers IPv6 packet

Step 1: IPv6 packet arrives at tunnel entry point
Step 2: Entry point wraps it in an IPv4 packet (encapsulation)
Step 3: IPv4 packet travels through the IPv4 internet
Step 4: Exit point unwraps the IPv6 packet (decapsulation)
Step 5: IPv6 packet delivered to destination
```

### 2.3 Types of Tunnels

| Type | Description | Example |
|------|-------------|---------|
| **6in4** | IPv6 inside IPv4 | Transitioning to IPv6 over IPv4 network |
| **GRE** | Generic Routing Encapsulation | Any protocol over any protocol |
| **IPSec** | Encrypted tunnel | VPN security |
| **MPLS** | Label-switched paths | ISP backbone |
| **SSH tunneling** | Application traffic over SSH | Bypassing firewalls |
| **VPN** | Encrypted tunnel for private traffic | Remote work |

### 2.4 GRE — Generic Routing Encapsulation

```
[IP Header | GRE Header | Passenger Packet]
            ↑ 4-byte GRE header identifies the encapsulated protocol

GRE allows ANY network protocol to be tunneled over ANY other:
  IPv6 over IPv4 ✅
  IPv4 over IPv4 (double encapsulation) ✅
  IPX over IP ✅
```

### 2.5 VPN Tunneling

**VPN (Virtual Private Network)** creates an encrypted tunnel between client and server:

```
Home PC ──Encrypted─────────────── VPN Server ──── Internet
         tunnel (IPSec/OpenVPN)

From Internet's view:
  Traffic looks like it's from VPN Server's IP, not Home PC
  All data is encrypted inside the tunnel
```

**Types of VPN:**
- **Site-to-site VPN**: Connects two corporate offices
- **Remote access VPN**: Employee connects to office network from home

### 2.6 Tunneling for IPv6 Transition

As the world migrates from IPv4 to IPv6, tunneling helps:

```
Techniques:
├── 6in4: Manual tunnel, IPv6 in IPv4 (Protocol 41)
├── 6to4: Automatic, uses special 2002::/16 prefix
├── Teredo: IPv6 in UDP in IPv4 (for NAT traversal)
└── ISATAP: Intra-Site Automatic Tunnel Addressing Protocol
```

---

## 3. NAT — Network Address Translation ⭐ IMPORTANT

### 3.1 The Problem NAT Solves

IPv4 has ~4.3 billion addresses — not enough for every device. Private IP addresses (RFC 1918) exist in abundance but are **not routable on the internet**.

**NAT allows many devices with private IPs to share a single public IP address.**

```
Home Network (private):          Internet (public):
  Laptop:    192.168.1.10 ─┐
  Phone:     192.168.1.11 ─┤  NAT Router  ──→  Public IP: 203.0.113.5
  Tablet:    192.168.1.12 ─┘  (translates)
  Smart TV:  192.168.1.13 ─┘
```

### 3.2 How NAT Works

**Scenario:** Home laptop (192.168.1.10) visits google.com (142.250.68.46)

#### Outbound (LAN → Internet)
```
Step 1: Laptop creates packet:
  Src IP:  192.168.1.10, Src Port: 5000
  Dst IP:  142.250.68.46, Dst Port: 80

Step 2: Packet reaches NAT router (192.168.1.1 / 203.0.113.5)

Step 3: NAT router translates:
  Src IP:  203.0.113.5  (replaces private IP with public IP)
  Src Port: 40001       (assigns new port to track connection)
  Dst IP:  142.250.68.46, Dst Port: 80

Step 4: NAT router records mapping:
  Table: 192.168.1.10:5000  ↔  203.0.113.5:40001

Step 5: Modified packet sent to Google
```

#### Inbound (Internet → LAN)
```
Step 1: Google sends reply:
  Src IP:  142.250.68.46, Src Port: 80
  Dst IP:  203.0.113.5,  Dst Port: 40001

Step 2: NAT router receives reply, looks up translation table:
  203.0.113.5:40001  →  192.168.1.10:5000

Step 3: NAT router translates:
  Dst IP:  192.168.1.10  (restores original private IP)
  Dst Port: 5000

Step 4: Packet forwarded to laptop
```

### 3.3 NAT Translation Table

```
┌──────────────────────────────────────────────────────────────────────┐
│                      NAT Translation Table                           │
├──────────────────────┬─────────────────────┬─────────────────────────┤
│   Inside Local       │   Inside Global     │   Outside Global        │
│  (Private IP:Port)   │  (Public IP:Port)   │   (Remote IP:Port)      │
├──────────────────────┼─────────────────────┼─────────────────────────┤
│  192.168.1.10:5000   │  203.0.113.5:40001  │  142.250.68.46:80       │
│  192.168.1.11:6500   │  203.0.113.5:40002  │  8.8.8.8:53             │
│  192.168.1.12:8080   │  203.0.113.5:40003  │  93.184.216.34:443      │
└──────────────────────┴─────────────────────┴─────────────────────────┘
```

### 3.4 Types of NAT

#### A. Static NAT (One-to-One)
- One private IP permanently maps to one public IP
- Used for hosting servers (web server, mail server)
- Does NOT conserve public IPs

```
192.168.1.10  ↔  203.0.113.10  (permanent mapping)
192.168.1.20  ↔  203.0.113.11  (permanent mapping)
```

#### B. Dynamic NAT
- Pool of public IPs; private IPs mapped to public IPs from the pool
- Mapping is temporary (session-based)
- Still one-to-one at any given time, but dynamic assignment

```
Pool: 203.0.113.10 – 203.0.113.20
192.168.1.10 → 203.0.113.10 (while active)
192.168.1.11 → 203.0.113.11 (while active)
```

#### C. PAT — Port Address Translation (NAT Overload) ⭐ MOST COMMON
- **Many private IPs → ONE public IP** (differentiated by port numbers)
- Also called **NAPT** (Network Address and Port Translation)
- What your home router does!

```
192.168.1.10:5000 → 203.0.113.5:40001  ─┐
192.168.1.11:6500 → 203.0.113.5:40002  ─┤ Same public IP!
192.168.1.12:8080 → 203.0.113.5:40003  ─┘
```

### 3.5 NAT Types Summary

| NAT Type | Mapping | Public IPs Needed | Use Case |
|---------|---------|------------------|---------|
| **Static** | 1 private ↔ 1 public | Many (1 per device) | Hosting servers |
| **Dynamic** | Pool-based | Many (pool) | General |
| **PAT (Overload)** | Many private → 1 public | **Just 1!** | **Home/office (most common)** |

### 3.6 NAT Advantages

| Advantage | Description |
|-----------|-------------|
| **Conserves IPs** | Many devices share one public IP |
| **Security** | Internal IPs hidden from internet (implicit firewall) |
| **Flexibility** | Change ISP without renumbering internal network |

### 3.7 NAT Disadvantages

| Disadvantage | Description |
|-------------|-------------|
| **Breaks end-to-end** | Internet's original design assumed global unique IPs |
| **P2P problems** | Hard to initiate connections TO NATted devices |
| **VoIP/Gaming issues** | Protocols that embed IPs in payload break |
| **Performance** | Translation adds latency and processing overhead |
| **Traceability** | Hard to identify which device made a request |
| **No IPv6 needed?** | NAT delayed IPv6 adoption — "good enough" for IPv4 |

### 3.8 NAT Traversal Techniques

When you need to reach a device behind NAT (P2P, VoIP, gaming):

| Technique | How It Works |
|-----------|-------------|
| **UPnP** | Device requests port forwarding from router automatically |
| **Port Forwarding** | Admin manually maps external port to internal device |
| **STUN** | Device discovers its public IP:port via a STUN server |
| **TURN** | Traffic relayed via a server (works behind all NAT types) |
| **ICE** | Combines STUN+TURN for WebRTC |
| **NAT hole punching** | Both peers connect to a rendezvous server, then directly |

---

## 4. Quick Comparison Summary

| Concept | What | Why | Where |
|---------|------|-----|-------|
| **Fragmentation** | Break large packets into smaller pieces | MTU limits on links | IPv4 routers, IPv6 sources |
| **Path MTU Discovery** | Find smallest MTU along path | Avoid fragmentation | IPv6, modern IPv4 |
| **Tunneling** | Encapsulate one protocol in another | Transport unsupported protocol | VPN, IPv6 over IPv4 |
| **NAT** | Translate private ↔ public IPs | IP address conservation | Home routers, enterprise |
| **PAT** | Many IPs → one IP via ports | Max address conservation | Most NAT deployments |

---

## 5. Interview Questions

**Q1: Why is fragmentation done at the network layer?**
> Different links along a path may have different MTUs. The network layer knows about routing and link properties, so it can break packets to fit the next link's MTU. Data Link Layer frames are link-specific and can't coordinate across multiple hops.

**Q2: What is the Fragment Offset and why is it in units of 8 bytes?**
> Fragment Offset (13 bits) tells the destination the position of the fragment within the original datagram. Since 13 bits can represent 8192 values, using 8-byte units allows representing offsets up to 65,536 bytes (8192 × 8), covering the max IPv4 datagram size.

**Q3: Why does IPv6 not allow routers to fragment packets?**
> Allowing routers to fragment adds latency and overhead. IPv6 requires source hosts to perform Path MTU Discovery — finding the smallest MTU along the path and sending packets that fit. If a router receives an oversized packet, it sends ICMP "Packet Too Big" back to the source.

**Q4: What is NAT and how does PAT work?**
> NAT translates private IP addresses to public IP addresses. PAT (Port Address Translation) allows many devices with different private IPs to share ONE public IP by assigning unique port numbers to each connection. The NAT table maps private IP:port to public IP:port, allowing correct delivery of return traffic.

**Q5: What are the disadvantages of NAT?**
> NAT breaks the internet's end-to-end principle (devices behind NAT can't be directly reached), complicates P2P and VoIP, adds processing overhead, and delays IPv6 adoption. It also makes it hard to trace which internal device made an external connection.

**Q6: What is tunneling and give an example?**
> Tunneling encapsulates one protocol's packet inside another's. Example: IPv6 packet wrapped in an IPv4 header so it can travel over IPv4 infrastructure that doesn't support IPv6. VPNs use tunneling (e.g., IPSec) to create encrypted private communication channels over public networks.

**Q7: What is the difference between Static NAT and PAT?**
> Static NAT maps one private IP permanently to one public IP (used for servers). PAT maps many private IPs to ONE public IP, distinguished by port numbers — this is what home routers use and is the most IP-efficient form of NAT.

**Q8: What is Path MTU Discovery?**
> A technique where the source sends packets with DF (Don't Fragment) bit set, then reduces packet size based on ICMP "Fragmentation Needed" messages from routers along the path. This discovers the minimum MTU of all links on the path, allowing the source to send optimally-sized packets without fragmentation.

---

*← Back to [Index](./README.md)*
