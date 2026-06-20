# 📡 Data Link Layer — Study Guide Index

> **Layer 2 of the OSI Model**
> The Data Link Layer is responsible for **node-to-node** (hop-to-hop) reliable delivery of data frames over a single physical link.

---

## 📚 Topics Covered

| File | Topics |
|------|--------|
| [01_Functions_and_Framing.md](./01_Functions_and_Framing.md) | Functions of DLL, Framing techniques |
| [02_Error_Detection_and_Correction.md](./02_Error_Detection_and_Correction.md) | Parity, CRC (⭐ IMPORTANT), Checksum |
| [03_MAC_Address_and_Ethernet.md](./03_MAC_Address_and_Ethernet.md) | MAC Address, Ethernet basics |
| [04_Multiple_Access_Protocols.md](./04_Multiple_Access_Protocols.md) | ALOHA, CSMA/CD |
| [05_Switching_Basics.md](./05_Switching_Basics.md) | Circuit, Packet, Message Switching |

---

## 🔑 Key Concepts at a Glance

```
Physical Layer (Layer 1)  ──→  Raw bits over cable/wireless
         ↓
Data Link Layer (Layer 2) ──→  Frames, MAC addressing, error detection
         ↓
Network Layer (Layer 3)   ──→  Packets, IP addressing, routing
```

### DLL Sub-layers
```
┌─────────────────────────────────┐
│   LLC — Logical Link Control    │  ← Error & Flow Control
├─────────────────────────────────┤
│   MAC — Media Access Control    │  ← Framing, Addressing, Access
└─────────────────────────────────┘
```

---

## ⚡ Quick Interview Cheat Sheet

| Concept | One-liner |
|---------|-----------|
| Framing | Wrapping packets into frames with headers/trailers |
| Parity | Add a bit so total 1s are even (or odd) |
| CRC | Polynomial division; remainder is the checksum |
| Checksum | Sum of data segments; complement used for verification |
| MAC | 48-bit hardware address, burned into NIC |
| Ethernet | CSMA/CD based wired LAN standard (IEEE 802.3) |
| Pure ALOHA | Send anytime; retry on collision (efficiency ~18.4%) |
| Slotted ALOHA | Send at slot start; retry on collision (efficiency ~36.8%) |
| CSMA/CD | Sense before send, detect collision, back off |
| Switching | Circuit / Packet / Message — how data traverses a network |

---

*Start with `01_Functions_and_Framing.md` →*
