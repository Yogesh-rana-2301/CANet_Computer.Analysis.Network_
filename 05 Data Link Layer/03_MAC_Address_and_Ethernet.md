# 🏷️ MAC Address & Ethernet

---

## 1. MAC Address (Media Access Control Address)

### 1.1 What is a MAC Address?

A **MAC address** is a **unique hardware identifier** assigned to a Network Interface Card (NIC). It operates at the **Data Link Layer (Layer 2)** and is used for communication **within the same local network (LAN)**.

Think of it as the **physical address** of a device — like a serial number burned into the hardware.

```
Your Device
┌────────────────────────────────────────┐
│  NIC (Network Interface Card)          │
│                                        │
│  MAC Address: AA:BB:CC:DD:EE:FF        │
│  ← Burned-In Address (BIA)            │
└────────────────────────────────────────┘
```

### 1.2 MAC Address Format

```
AA : BB : CC : DD : EE : FF
│─────────────│ │─────────────│
  OUI (24 bits)    Device ID (24 bits)
  (Manufacturer)   (Unique per device)

Total: 48 bits = 6 bytes = 12 hexadecimal digits
```

**OUI** = Organizationally Unique Identifier — assigned by IEEE to manufacturers.

**Examples:**
| OUI | Manufacturer |
|-----|-------------|
| `00:50:56` | VMware |
| `00:1A:2B` | Apple |
| `FC:FB:FB` | Cisco |

### 1.3 MAC Address Notation

| Format | Example |
|--------|---------|
| Colon-separated (Unix) | `AA:BB:CC:DD:EE:FF` |
| Hyphen-separated (Windows) | `AA-BB-CC-DD-EE-FF` |
| Dot-separated (Cisco) | `AABB.CCDD.EEFF` |

### 1.4 Special MAC Addresses

| Address | Type | Purpose |
|---------|------|---------|
| `FF:FF:FF:FF:FF:FF` | **Broadcast** | Sent to ALL devices on the LAN |
| `01:00:5E:xx:xx:xx` | **Multicast** | Sent to a group of devices (IPv4 multicast) |
| Unique address | **Unicast** | Sent to one specific device |

### 1.5 Important Bits in First Byte

```
First Byte: XX : BB : CC : DD : EE : FF
             │└── Bit 1: 0 = Unicast, 1 = Multicast/Broadcast
             └─── Bit 0: 0 = Globally unique (OUI), 1 = Locally administered
```

### 1.6 MAC vs. IP Address

| Feature | MAC Address | IP Address |
|---------|------------|------------|
| **Layer** | Data Link (L2) | Network (L3) |
| **Length** | 48 bits (6 bytes) | 32 bits (IPv4) / 128 bits (IPv6) |
| **Assigned by** | Manufacturer (hardware) | Network admin / DHCP (software) |
| **Scope** | Local network only | Global (internet-wide) |
| **Changes?** | No (usually permanent) | Yes (can change) |
| **Purpose** | LAN delivery (hop-by-hop) | End-to-end delivery |
| **Example** | `AA:BB:CC:DD:EE:FF` | `192.168.1.1` |

> **Analogy**: MAC = your name (fixed), IP = your home address (can change if you move).

### 1.7 How MAC and IP Work Together (ARP)

When your computer wants to send data to `192.168.1.5` on the same LAN:

1. **Check ARP cache** — does it already know the MAC for `192.168.1.5`?
2. If not → **Broadcast ARP request**: "Who has IP 192.168.1.5? Tell me your MAC!"
3. Device with that IP **replies with its MAC address**.
4. Sender stores in ARP cache, then sends frame to that MAC.

```
Device A                                    Device B
IP: 192.168.1.1                            IP: 192.168.1.5
MAC: AA:BB:CC:DD:EE:01                     MAC: AA:BB:CC:DD:EE:05

A broadcasts: "Who has 192.168.1.5?"
                     ────────────────────────────→ (broadcast to all)
B responds: "I have 192.168.1.5. My MAC is AA:BB:CC:DD:EE:05"
                     ←────────────────────────────

A now sends:
  Dest MAC: AA:BB:CC:DD:EE:05  | Dest IP: 192.168.1.5
```

### 1.8 MAC Address in Frame Forwarding

```
Frame traveling across networks:

  ┌────────────────────────────────────────────────────────────────┐
  │ Dest MAC (changes)  | Src MAC (changes)  | Dest IP | Src IP   │
  │    per hop                per hop        | (FIXED) | (FIXED)  │
  └────────────────────────────────────────────────────────────────┘

Host A → Router R1:  Dest MAC = R1's MAC, Src MAC = A's MAC
Router R1 → Router R2:  Dest MAC = R2's MAC, Src MAC = R1's MAC
Router R2 → Host B:  Dest MAC = B's MAC, Src MAC = R2's MAC
```

> **Key**: IP addresses remain constant end-to-end. MAC addresses change at every hop.

---

## 2. Ethernet

### 2.1 What is Ethernet?

Ethernet is the most widely used **wired LAN technology**, standardized as **IEEE 802.3**. It defines:
- Physical medium (cables, connectors)
- Frame format
- Access method (CSMA/CD)

### 2.2 Brief History

| Year | Standard | Speed |
|------|----------|-------|
| 1983 | 10BASE-T (IEEE 802.3) | 10 Mbps |
| 1995 | Fast Ethernet (802.3u) | 100 Mbps |
| 1999 | Gigabit Ethernet (802.3ab) | 1 Gbps |
| 2002 | 10 Gigabit Ethernet (802.3ae) | 10 Gbps |
| 2016 | 400 Gigabit Ethernet | 400 Gbps |

### 2.3 Ethernet Frame Format (IEEE 802.3)

```
┌──────────┬─────┬──────────┬──────────┬──────────┬──────────────────┬──────────┐
│ Preamble │ SFD │ Dest MAC │ Src MAC  │  Type/   │     Data         │   FCS    │
│  7 bytes │1 B  │  6 bytes │  6 bytes │  Length  │  (46-1500 bytes) │  4 bytes │
│          │     │          │          │  2 bytes │                  │ (CRC-32) │
└──────────┴─────┴──────────┴──────────┴──────────┴──────────────────┴──────────┘
```

| Field | Size | Description |
|-------|------|-------------|
| **Preamble** | 7 bytes | `10101010...` alternating bits for clock sync |
| **SFD** (Start Frame Delimiter) | 1 byte | `10101011` — signals start of frame |
| **Destination MAC** | 6 bytes | Recipient's MAC address |
| **Source MAC** | 6 bytes | Sender's MAC address |
| **Type/EtherType** | 2 bytes | Payload protocol (`0x0800`=IPv4, `0x0806`=ARP) |
| **Data** | 46–1500 bytes | Actual payload (padded to min 46 bytes) |
| **FCS** | 4 bytes | CRC-32 error check |

**Minimum frame size**: 64 bytes (ensures collision detection works in CSMA/CD)
**Maximum frame size**: 1518 bytes (called MTU = Maximum Transmission Unit of 1500 bytes for data)

### 2.4 Why Minimum Frame Size of 64 Bytes?

This is related to **CSMA/CD** collision detection. A sender must still be transmitting when a collision signal (jam) arrives back. For a 10 Mbps Ethernet with max cable length, the round-trip propagation time ≈ **51.2 µs**, during which 512 bits (= 64 bytes) can be sent.

```
Sender ─────────────────────────────→ (sends frame)
                      ← ← ← ← ← ← ← (collision jam travels back)
        ↑─────────────────────────────↑
              Must still be sending!
           This takes 51.2 µs for 64 bytes at 10 Mbps
```

### 2.5 Ethernet Topology Evolution

```
1980s: Bus Topology (coaxial cable — 10BASE2, 10BASE5)
  All devices share one cable — any signal reaches all devices
  ┌────────────────────────────────────────────┐
  │──────┬──────┬──────┬──────┬──────┬─────── │
         PC     PC     PC     PC     PC

1990s-Today: Star Topology (twisted pair — 10BASE-T, 100BASE-TX)
  All devices connect to a central HUB or SWITCH
       ┌──── PC
       ├──── PC
  SWITCH├──── PC
       ├──── PC
       └──── PC
```

### 2.6 Hub vs. Switch

| Feature | Hub | Switch |
|---------|-----|--------|
| **OSI Layer** | Layer 1 (Physical) | Layer 2 (Data Link) |
| **Understands** | Nothing (just amplifies) | MAC addresses |
| **Forwarding** | Broadcasts to all ports | Sends only to destination port |
| **Collisions** | Single collision domain | Each port = separate collision domain |
| **Bandwidth** | Shared | Dedicated per port |
| **Intelligence** | None | MAC address table |

### 2.7 Basic Ethernet Operation

1. **Sender** creates a frame with destination MAC and its own source MAC.
2. **Sends frame** into the network.
3. **Switch** receives the frame, looks up the destination MAC in its MAC table.
   - If found → forward to that specific port only.
   - If not found → flood to all ports (except where it came from).
4. **Receiver** gets the frame, checks dest MAC matches its own → accepts it.
5. **FCS** is verified — if CRC check fails → frame discarded.

### 2.8 EtherType Values

| Value | Protocol |
|-------|---------|
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| `0x8100` | VLAN tagged frame (802.1Q) |
| `0x0835` | RARP |

---

## 3. Interview Questions

**Q1: What is a MAC address and where is it used?**
> A 48-bit hardware address burned into a NIC, used for frame delivery within a local network (Layer 2). It identifies devices at the Data Link Layer.

**Q2: What is the difference between MAC and IP addresses?**
> MAC is a physical, fixed, 48-bit identifier for a NIC (Layer 2, local scope). IP is a logical, assignable address (Layer 3, global scope). MAC addresses change at each hop; IP addresses stay fixed end-to-end.

**Q3: What happens when a switch receives a frame for an unknown MAC?**
> The switch **floods** the frame out of all ports except the incoming port. When the destination replies, the switch learns its MAC and port, updating its MAC table.

**Q4: Why does an Ethernet frame have a minimum size of 64 bytes?**
> To ensure CSMA/CD collision detection works correctly. The sender must still be transmitting when the collision jam signal returns (round-trip propagation delay ≈ 512 bits at 10 Mbps).

**Q5: What is ARP and why is it needed?**
> ARP (Address Resolution Protocol) maps IP addresses to MAC addresses. When a device knows the destination IP but not its MAC, it broadcasts an ARP request. The device with that IP responds with its MAC address.

**Q6: What does the FCS field in an Ethernet frame contain?**
> A 4-byte CRC-32 checksum. The receiver recalculates it and compares — if it doesn't match, the frame is discarded as corrupted.

**Q7: What is the difference between a Hub and a Switch?**
> A hub (Layer 1) broadcasts all incoming frames to all ports — all devices share one collision domain. A switch (Layer 2) learns MAC addresses and forwards frames only to the correct port, creating separate collision domains per port.

---

*Next: [04 — Multiple Access Protocols →](./04_Multiple_Access_Protocols.md)*
