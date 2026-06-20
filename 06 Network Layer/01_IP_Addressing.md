# 🏠 IP Addressing — IPv4, IPv6 & Subnetting

> ⭐ **VERY IMPORTANT** — Subnetting questions are extremely common in networking interviews!

---

## 1. IPv4 — Structure & Format

### 1.1 What is an IP Address?

An **IP (Internet Protocol) address** is a **logical, 32-bit identifier** assigned to every device on a network. Unlike MAC addresses (hardware, fixed), IP addresses are **software-assigned** and can change.

### 1.2 IPv4 Address Format

```
IPv4 = 32 bits = 4 octets (bytes), written in dotted-decimal notation

  192    .   168    .    1    .    1
10000000   10101000  00000001  00000001
  ↑ 8 bits   ↑ 8 bits  ↑ 8 bits  ↑ 8 bits
                    = 32 bits total
```

**Range of each octet**: 0 – 255 (since 2⁸ = 256 values)
**Total IPv4 addresses**: 2³² ≈ **4.3 billion**

### 1.3 Classful Addressing (Historical — Still Tested!)

Before CIDR, IP addresses were divided into fixed classes:

```
Class A:  0xxxxxxx . xxxxxxxx . xxxxxxxx . xxxxxxxx
          Network  │────────── Host ──────────────│
          8 bits   │         24 bits               │

Class B:  10xxxxxx . xxxxxxxx . xxxxxxxx . xxxxxxxx
          ─── Network ──────  │──── Host ──────────│
               16 bits        │      16 bits        │

Class C:  110xxxxx . xxxxxxxx . xxxxxxxx . xxxxxxxx
          ────────── Network ───────────│── Host ───│
                    24 bits             │  8 bits   │

Class D:  1110xxxx ... (Multicast — not for hosts)
Class E:  1111xxxx ... (Experimental — reserved)
```

| Class | First Octet Range | Network bits | Host bits | Default Mask | Hosts per network |
|-------|------------------|-------------|----------|-------------|------------------|
| **A** | 1 – 126 | 8 | 24 | `255.0.0.0` (/8) | 2²⁴ − 2 = **16,777,214** |
| **B** | 128 – 191 | 16 | 16 | `255.255.0.0` (/16) | 2¹⁶ − 2 = **65,534** |
| **C** | 192 – 223 | 24 | 8 | `255.255.255.0` (/24) | 2⁸ − 2 = **254** |
| **D** | 224 – 239 | — | — | — | Multicast |
| **E** | 240 – 255 | — | — | — | Reserved |

> **Note**: `127.x.x.x` is reserved for loopback (127.0.0.1 = localhost). Class A starts at 1, not 0.

### 1.4 Special IPv4 Addresses

| Address | Purpose |
|---------|---------|
| `0.0.0.0` | This host (unspecified) |
| `127.0.0.1` | Loopback (localhost) |
| `255.255.255.255` | Limited broadcast (all hosts on local network) |
| `x.x.x.255` | Directed broadcast to a subnet |
| `x.x.x.0` | Network address (not usable for hosts) |

### 1.5 Private IP Address Ranges (RFC 1918)

These addresses are **not routable on the internet** — used in private networks:

| Range | Class | Prefix | Use |
|-------|-------|--------|-----|
| `10.0.0.0` – `10.255.255.255` | A | `/8` | Large orgs |
| `172.16.0.0` – `172.31.255.255` | B | `/12` | Medium orgs |
| `192.168.0.0` – `192.168.255.255` | C | `/16` | Home/small networks |

> Private IPs need **NAT** to communicate with the internet.

### 1.6 IPv4 Header Structure

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├───────┬───────┬───────────────────────┬───────────────────────────┤
│Version│  IHL  │  DSCP / ToS           │    Total Length           │
├───────┴───────┴───────────────────────┴───────────────────────────┤
│         Identification                │Flags│  Fragment Offset     │
├───────────────────────────────────────┴─────┴──────────────────────┤
│      TTL          │     Protocol      │    Header Checksum         │
├───────────────────┴───────────────────┴────────────────────────────┤
│                         Source IP Address                          │
├────────────────────────────────────────────────────────────────────┤
│                      Destination IP Address                        │
├────────────────────────────────────────────────────────────────────┤
│                    Options (if IHL > 5)                            │
└────────────────────────────────────────────────────────────────────┘
```

| Field | Size | Description |
|-------|------|-------------|
| **Version** | 4 bits | `4` for IPv4 |
| **IHL** | 4 bits | Header length in 32-bit words (min=5 → 20 bytes) |
| **Total Length** | 16 bits | Total packet size (header + data), max 65535 bytes |
| **Identification** | 16 bits | ID for fragmentation reassembly |
| **Flags** | 3 bits | DF (Don't Fragment), MF (More Fragments) |
| **Fragment Offset** | 13 bits | Position of fragment in original datagram |
| **TTL** | 8 bits | Decremented at each hop; packet dropped when TTL=0 |
| **Protocol** | 8 bits | Upper layer: `6`=TCP, `17`=UDP, `1`=ICMP |
| **Header Checksum** | 16 bits | Error check for header only |
| **Source IP** | 32 bits | Sender's IP address |
| **Dest IP** | 32 bits | Receiver's IP address |

**Minimum header size**: 20 bytes (IHL=5, no options)

---

## 2. Subnetting ⭐ VERY IMPORTANT

### 2.1 What is Subnetting?

Subnetting divides a large network into smaller **sub-networks (subnets)** to:
- Better organize devices
- Reduce broadcast traffic (each subnet = its own broadcast domain)
- Improve security (isolate departments)
- Efficiently use IP address space

```
Company Network: 192.168.1.0/24  (256 addresses)
         │
         ├──→ IT Dept:  192.168.1.0/26   (64 addresses)
         ├──→ HR Dept:  192.168.1.64/26  (64 addresses)
         ├──→ Sales:    192.168.1.128/26 (64 addresses)
         └──→ Mgmt:     192.168.1.192/26 (64 addresses)
```

### 2.2 Subnet Mask

A **subnet mask** is a 32-bit number that divides an IP address into:
- **Network portion** (1s) — identifies the network
- **Host portion** (0s) — identifies individual devices

```
IP Address:   192.168.1.100   =  11000000.10101000.00000001.01100100
Subnet Mask:  255.255.255.0   =  11111111.11111111.11111111.00000000
                                  ──────────────────────────  ────────
                                       Network (24 bits)      Host (8 bits)

AND operation (IP & Mask) → Network Address:
  11000000.10101000.00000001.01100100
& 11111111.11111111.11111111.00000000
= 11000000.10101000.00000001.00000000
= 192.168.1.0  ← Network Address
```

### 2.3 CIDR Notation (Classless Inter-Domain Routing)

CIDR replaces classful addressing. The **prefix length** (after `/`) tells how many bits are the network portion.

```
192.168.1.0/24
            ↑ 24 bits are network bits → 8 bits left for hosts
```

**Conversion table:**
| CIDR | Subnet Mask | Network Bits | Host Bits | Total Addresses | Usable Hosts |
|------|------------|-------------|---------|-----------------|-------------|
| /8   | 255.0.0.0 | 8 | 24 | 16,777,216 | 16,777,214 |
| /16  | 255.255.0.0 | 16 | 16 | 65,536 | 65,534 |
| /24  | 255.255.255.0 | 24 | 8 | 256 | **254** |
| /25  | 255.255.255.128 | 25 | 7 | 128 | **126** |
| /26  | 255.255.255.192 | 26 | 6 | 64 | **62** |
| /27  | 255.255.255.224 | 27 | 5 | 32 | **30** |
| /28  | 255.255.255.240 | 28 | 4 | 16 | **14** |
| /29  | 255.255.255.248 | 29 | 3 | 8 | **6** |
| /30  | 255.255.255.252 | 30 | 2 | 4 | **2** |
| /32  | 255.255.255.255 | 32 | 0 | 1 | 0 (host route) |

> **Formula**: Usable hosts = 2^(host bits) − 2
> (subtract 2: one for Network Address, one for Broadcast Address)

### 2.4 Key Formulas

$$\text{Number of Hosts} = 2^h - 2 \quad \text{where } h = \text{host bits}$$

$$\text{Number of Subnets} = 2^s \quad \text{where } s = \text{borrowed bits}$$

$$\text{Block Size} = 2^h \quad \text{(total addresses in subnet)}$$

### 2.5 Finding Network Details — Step by Step

**Example**: Given IP `192.168.10.130/26`, find:
- Network address
- Broadcast address
- First usable host
- Last usable host
- Number of hosts

**Step 1: Identify host bits**
```
/26 → 32 − 26 = 6 host bits
Block size = 2^6 = 64 addresses
```

**Step 2: Find the subnet**
```
Subnet mask: /26 = 255.255.255.192 (last octet = 11000000 = 192)
Interesting octet: 4th (last)
Subnet boundaries (multiples of 64): 0, 64, 128, 192, 256...
130 falls in the range 128 – 191 → subnet starting at 128
```

**Step 3: Calculate all values**
```
Network Address:     192.168.10.128   ← First address (.128)
First Usable Host:   192.168.10.129   ← Network + 1
Last Usable Host:    192.168.10.190   ← Broadcast − 1
Broadcast Address:   192.168.10.191   ← Last address (.128 + 64 − 1)
Number of Hosts:     2^6 − 2 = 62
```

### 2.6 Subnetting Examples Table

| Network | CIDR | Subnet Mask | Hosts | Network Addr | Broadcast |
|---------|------|------------|-------|-------------|-----------|
| 10.0.0.0 | /8 | 255.0.0.0 | 16,777,214 | 10.0.0.0 | 10.255.255.255 |
| 172.16.0.0 | /16 | 255.255.0.0 | 65,534 | 172.16.0.0 | 172.16.255.255 |
| 192.168.1.0 | /24 | 255.255.255.0 | 254 | 192.168.1.0 | 192.168.1.255 |
| 192.168.1.0 | /25 | 255.255.255.128 | 126 | 192.168.1.0 | 192.168.1.127 |
| 192.168.1.128 | /25 | 255.255.255.128 | 126 | 192.168.1.128 | 192.168.1.255 |

### 2.7 Subnetting Practice: Dividing a /24 into Subnets

**Task**: Divide `192.168.5.0/24` into 4 equal subnets

```
We need 4 subnets → 2^s = 4 → s = 2 borrowed bits
New prefix: /24 + 2 = /26
Host bits remaining: 6 → each subnet has 2^6 = 64 addresses, 62 usable hosts

Subnet 1:  192.168.5.0/26    hosts: .1 – .62    broadcast: .63
Subnet 2:  192.168.5.64/26   hosts: .65 – .126  broadcast: .127
Subnet 3:  192.168.5.128/26  hosts: .129 – .190 broadcast: .191
Subnet 4:  192.168.5.192/26  hosts: .193 – .254 broadcast: .255
```

### 2.8 VLSM — Variable Length Subnet Masking

Instead of equal-sized subnets, VLSM allows **different sizes** to match actual needs.

```
Network: 192.168.1.0/24 — needs:
  Dept A: 100 hosts → /25 (126 usable) → 192.168.1.0/25
  Dept B: 50 hosts  → /26 (62 usable)  → 192.168.1.128/26
  Dept C: 25 hosts  → /27 (30 usable)  → 192.168.1.192/27
  Link:   2 hosts   → /30 (2 usable)   → 192.168.1.224/30
```

---

## 3. IPv6 — Basics

### 3.1 Why IPv6?

IPv4 has ~4.3 billion addresses — exhausted by ~2011. IPv6 provides:
- **128-bit addresses** → 2¹²⁸ ≈ **340 undecillion** addresses
- No need for NAT (enough addresses for every device)
- Built-in IPSec (security)
- Simplified header (faster routing)
- No broadcast (uses multicast instead)
- Stateless Address Autoconfiguration (SLAAC)

### 3.2 IPv6 Address Format

```
128 bits = 8 groups of 16 bits, written in hexadecimal, separated by colons

2001:0db8:85a3:0000:0000:8a2e:0370:7334
─────┤────┤────┤────┤────┤────┤────┤────
  16   16   16   16   16   16   16   16 bits each
```

**Simplification Rules:**

1. **Remove leading zeros** in each group:
   ```
   0000 → 0
   0db8 → db8
   ```

2. **Replace one consecutive run of all-zero groups with `::`**:
   ```
   2001:0db8:0000:0000:0000:0000:0370:7334
   → 2001:db8::370:7334
   ```
   > `::` can only be used **once** in an address!

**Examples:**
| Full Address | Compressed |
|-------------|-----------|
| `2001:0db8:0000:0000:0000:0000:0000:0001` | `2001:db8::1` |
| `fe80:0000:0000:0000:0202:b3ff:fe1e:8329` | `fe80::202:b3ff:fe1e:8329` |
| `0000:0000:0000:0000:0000:0000:0000:0001` | `::1` (loopback) |
| `0000:0000:...0000` | `::` (unspecified) |

### 3.3 IPv6 Address Types

| Type | Prefix | Description |
|------|--------|-------------|
| **Unicast** (Global) | `2000::/3` | Routable internet addresses |
| **Link-local** | `fe80::/10` | Auto-assigned, only valid on local link |
| **Loopback** | `::1/128` | Same as 127.0.0.1 in IPv4 |
| **Unspecified** | `::/128` | Like 0.0.0.0 in IPv4 |
| **Multicast** | `ff00::/8` | Replaces broadcast |
| **Unique Local** | `fc00::/7` | Like private IPs (RFC 1918) |

### 3.4 IPv6 Header vs IPv4 Header

| Field | IPv4 | IPv6 |
|-------|------|------|
| **Header size** | 20–60 bytes | Fixed **40 bytes** |
| **Address size** | 32 bits | 128 bits |
| **Fragmentation** | By routers & hosts | **Only by source host** |
| **Checksum** | ✅ Yes (header) | ❌ No (offloaded to transport) |
| **TTL** | TTL field | **Hop Limit** field |
| **Options** | Yes (variable) | Extension headers |
| **Broadcast** | ✅ Yes | ❌ No (multicast instead) |
| **IPSec** | Optional | Mandatory support |

### 3.5 IPv4 vs IPv6 Summary

| Feature | IPv4 | IPv6 |
|---------|------|------|
| Address length | 32 bits | 128 bits |
| Notation | Dotted decimal | Hexadecimal with colons |
| Total addresses | ~4.3 billion | ~340 undecillion |
| Header size | Variable (20-60B) | Fixed (40B) |
| Fragmentation | Routers + hosts | Source host only |
| NAT needed | Yes | No |
| Configuration | Manual/DHCP | SLAAC or DHCPv6 |
| Broadcast | Yes | No (multicast) |
| Security | Optional IPSec | Mandatory IPSec support |

---

## 4. Interview Questions

**Q1: What is CIDR notation?**
> CIDR (Classless Inter-Domain Routing) notation specifies an IP address followed by a slash and the number of network bits (e.g., `192.168.1.0/24`). It replaces classful addressing to allow flexible subnet sizes.

**Q2: How many usable hosts does a /27 subnet have?**
> /27 → 32−27 = 5 host bits → 2⁵−2 = **30 usable hosts**.

**Q3: What is the difference between network address and broadcast address?**
> The network address (all host bits = 0) identifies the subnet itself. The broadcast address (all host bits = 1) sends a packet to all hosts in the subnet. Neither can be assigned to a host.

**Q4: Given IP 10.20.30.40/20 — what is the network address?**
> /20 means 20 network bits. The 3rd octet provides bits 17–24. With /20, the last 4 bits of the 3rd octet are host bits. 30 in binary = `0001 1110`. Network bits keep first 4 → `0001 0000` = 16. Network: `10.20.16.0/20`.

**Q5: Why do we subtract 2 from host addresses?**
> One address is reserved as the **Network Address** (all host bits = 0) and one as the **Broadcast Address** (all host bits = 1). Neither can be assigned to a host.

**Q6: What is VLSM?**
> Variable Length Subnet Masking allows subnets of different sizes within the same network, efficiently allocating addresses based on actual host requirements instead of wasting addresses with fixed-size subnets.

**Q7: Why was IPv6 introduced?**
> IPv4 address exhaustion (~4.3B addresses ran out). IPv6 provides 2¹²⁸ addresses, built-in IPSec, simplified headers, no NAT needed, and eliminates broadcast traffic.

---

*Next: [02 — Core Protocols (ICMP & ARP) →](./02_Core_Protocols.md)*
