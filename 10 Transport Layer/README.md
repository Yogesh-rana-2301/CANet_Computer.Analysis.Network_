# 🚀 Transport Layer — Study Guide Index

> **OSI Layer 4** ⭐ **VERY HIGH PRIORITY** — The most tested layer in software engineering interviews.
> Responsible for **process-to-process** (end-to-end) reliable delivery of data between applications.

---

## 📚 Files in This Section

| File | Topics |
|------|--------|
| [01_Basics.md](./01_Basics.md) | Functions, Process-to-Process delivery, Ports, Multiplexing |
| [02_TCP_Deep_Dive.md](./02_TCP_Deep_Dive.md) | TCP features, 3-way handshake, 4-way termination, Seq/ACK, Sliding Window, Flow & Congestion Control |
| [03_UDP_and_Comparison.md](./03_UDP_and_Comparison.md) | UDP features, TCP vs UDP (⭐ VERY IMPORTANT) |

---

## 🔑 Layer Context

```
Application (L7)  →  HTTP, DNS, FTP, SMTP
                           │
Transport   (L4)  →  TCP / UDP         ← OUR FOCUS
                           │
Network     (L3)  →  IP, ICMP, ARP
                           │
Data Link   (L2)  →  Ethernet, MAC
                           │
Physical    (L1)  →  Bits, cables, signals
```

---

## ⚡ Transport Layer Master Cheat Sheet

### TCP at a Glance
| Feature | Detail |
|---------|--------|
| Connection | 3-way handshake (SYN → SYN-ACK → ACK) |
| Termination | 4-way (FIN → ACK → FIN → ACK) |
| Reliability | Seq numbers + ACKs + retransmission |
| Flow control | Receive Window (rwnd) |
| Congestion control | Slow Start → AIMD (CWND) |
| Header size | 20 bytes minimum |
| Port range | 0–65535 |

### UDP at a Glance
| Feature | Detail |
|---------|--------|
| Connection | None (connectionless) |
| Reliability | None (best-effort) |
| Header size | 8 bytes (fixed) |
| Use case | DNS, VoIP, video streaming, gaming |

### TCP vs UDP — One-liner
> TCP = Reliable, ordered, slow. UDP = Unreliable, fast, lightweight.

---

*Start with [01 — Basics →](./01_Basics.md)*
