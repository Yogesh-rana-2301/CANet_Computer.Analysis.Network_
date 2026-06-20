# 🌐 Network Layer — Study Guide Index

> **OSI Layer 3** ⭐ HIGH PRIORITY — This is one of the most heavily tested layers in interviews!
> Responsible for **end-to-end packet delivery** across multiple networks (internetworking).

---

## 📚 Files in This Section

| File | Topics |
|------|--------|
| [01_IP_Addressing.md](./01_IP_Addressing.md) | IPv4 structure, IPv6 basics, Subnetting, CIDR, Subnet masks |
| [02_Core_Protocols.md](./02_Core_Protocols.md) | ICMP, ARP (⭐ VERY IMPORTANT) |
| [03_Routing.md](./03_Routing.md) | Distance Vector, Link State, RIP vs OSPF vs BGP, Count-to-infinity |
| [04_Other_Concepts.md](./04_Other_Concepts.md) | Fragmentation, Tunneling, NAT (⭐ IMPORTANT) |

---

## 🗺️ What the Network Layer Does

```
Application  ─┐
Transport    ─┤                                  ┌─ Application
Network   ◄───┤  Responsible for routing packets  ├─► Network
Data Link    ─┘  from source to destination       └─ Data Link
Physical                                             Physical

Source Host                                    Destination Host
    │                                               ▲
    │  [IP Packet]                                  │
    ▼                                               │
Router 1 ──────────→ Router 2 ──────────→ Router 3
(makes routing decision at each hop)
```

---

## 🔑 Key Responsibilities

| Function | Description |
|---------|-------------|
| **Logical Addressing** | IP addresses identify source & destination globally |
| **Routing** | Find the best path from source to destination |
| **Packet Forwarding** | Move packet from one interface to next hop |
| **Fragmentation** | Break large packets to fit MTU of smaller links |
| **Internetworking** | Connect heterogeneous networks |

---

## ⚡ Network Layer Cheat Sheet

| Concept | Key Fact |
|---------|---------|
| IPv4 | 32-bit address, 4 billion addresses |
| IPv6 | 128-bit address, 340 undecillion addresses |
| Subnet mask /24 | 256 addresses, 254 usable hosts |
| CIDR | Classless Inter-Domain Routing |
| ARP | Maps IP → MAC (Layer 3 → Layer 2) |
| ICMP | Error reporting (ping, traceroute) |
| NAT | Maps private IPs to one public IP |
| RIP | Distance vector, max 15 hops |
| OSPF | Link state, uses Dijkstra, no hop limit |
| BGP | Internet's backbone routing protocol |
| Count-to-Infinity | Distance Vector convergence problem |
| TTL | Time to Live — prevents infinite routing loops |

---

*Start with [01 — IP Addressing →](./01_IP_Addressing.md)*
