# 🔧 Functions of the Data Link Layer & Framing

> **OSI Layer 2** | Hop-to-hop delivery between directly connected nodes

---

## 1. What is the Data Link Layer?

The Data Link Layer (DLL) sits between the **Physical Layer** (Layer 1) and the **Network Layer** (Layer 3). While the Physical Layer transmits raw bits, the DLL organizes those bits into meaningful units called **frames** and ensures their reliable delivery across a **single link** (not end-to-end — that's Transport layer's job).

```
Sender                              Receiver
  │                                    │
  ▼  Network Layer (Packets)           ▼
┌────────────────────────────────────────┐
│          Data Link Layer               │  ← Our focus
│   Frames: Header + Data + Trailer     │
└────────────────────────────────────────┘
  │  Physical Layer (Bits/Signals)      │
  └────────────────────────────────────▶
```

---

## 2. Functions of the Data Link Layer

### 2.1 Framing
Divides the stream of bits (received from Network layer) into manageable units called **frames**. Adds a header and trailer to demarcate each frame.

### 2.2 Physical Addressing (MAC Addressing)
Adds the **source and destination MAC addresses** in the frame header so the frame can be delivered to the correct machine on the local network.

```
Frame Header contains:
  ┌─────────────────┬──────────────────┐
  │ Dest MAC Addr   │  Src MAC Addr    │
  └─────────────────┴──────────────────┘
```

### 2.3 Error Detection & Correction
Detects (and sometimes corrects) errors that occur during transmission over the physical medium. Techniques: **Parity, CRC, Checksum**.

### 2.4 Flow Control
Prevents a fast sender from overwhelming a slow receiver by regulating the rate of data transmission.
- **Stop-and-Wait** — send one frame, wait for ACK
- **Sliding Window** — send multiple frames before needing ACK

### 2.5 Access Control (MAC)
When multiple devices share a common channel, DLL determines which device can use the channel at a given time.
- Protocols: ALOHA, CSMA/CD, Token Ring

### 2.6 Error Control
Handles acknowledgments (ACKs) and retransmissions when frames are lost or corrupted.
- **ARQ (Automatic Repeat Request)** — Stop-and-Wait ARQ, Go-Back-N, Selective Repeat

---

## 3. Sub-layers of the Data Link Layer

The DLL is divided into **two sub-layers** (IEEE 802 standard):

```
┌───────────────────────────────────────────────────────────┐
│              DATA LINK LAYER                              │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │   LLC — Logical Link Control (IEEE 802.2)           │  │
│  │   • Error control, Flow control                     │  │
│  │   • Interface with the Network Layer                │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │   MAC — Media Access Control (IEEE 802.3/11/15…)   │  │
│  │   • Framing, Physical Addressing                    │  │
│  │   • Multiple access (CSMA/CD, CSMA/CA)             │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

| Sub-layer | Full Name | Responsibility |
|-----------|-----------|---------------|
| **LLC** | Logical Link Control | Flow control, error control, multiplexing protocols |
| **MAC** | Media Access Control | Framing, MAC addressing, medium access |

---

## 4. Framing

### 4.1 What is Framing?
Framing is the process of **packaging data (from the Network layer) into frames** by adding a header and a trailer. The receiver uses these to identify where each frame starts and ends.

```
Network Layer Packet
        │
        ▼ (Framing)
┌───────┬────────────────────────┬─────────┐
│Header │       Data (Payload)   │ Trailer │
└───────┴────────────────────────┴─────────┘
 ← Frame ─────────────────────────────────→
```

### 4.2 Why Framing?
- Physical layer sends/receives raw bits — it has no notion of where a message starts or ends.
- Framing gives **structure** to the bitstream.
- Enables **error detection** (trailer carries checksum/CRC).
- Enables **addressing** (header carries MAC addresses).

### 4.3 Framing Techniques

#### A. Fixed-Size Framing
- Every frame has a **fixed, predetermined length**.
- No need for start/end delimiters.
- **Problem**: Wasted space if data is small; internal fragmentation.
- **Example**: ATM cells (53 bytes — 5 header + 48 data)

```
│◄── 53 bytes ──►│◄── 53 bytes ──►│◄── 53 bytes ──►│
└────────────────┘└────────────────┘└────────────────┘
   ATM Cell           ATM Cell           ATM Cell
```

#### B. Variable-Size Framing
Frame length varies based on data. Two main methods:

##### B1. Character/Byte Count
- First field of header stores the **total length** of the frame (in bytes).
- Receiver reads that many bytes, then looks for the next frame.
- **Problem**: If the count field is corrupted, the receiver loses sync — **fatal error**.

```
┌───────┬──────────────┐┌───────┬─────────────────┐
│Count=5│ D A T A     ││Count=7│ D A T A   ··    │
└───────┴──────────────┘└───────┴─────────────────┘
```

##### B2. Byte Stuffing (Character Stuffing)
- Special **FLAG** byte (e.g., `01111110`) marks frame start and end.
- If FLAG appears in data → insert an **ESC (Escape)** byte before it.
- Receiver strips ESC bytes to recover original data.
- **Problem**: ESC in data needs another ESC → overhead increases.

```
Original data: ... FLAG ...
After stuffing: ... ESC FLAG ...

Original data: ... ESC ...
After stuffing: ... ESC ESC ...
```

**Example (PPP protocol uses this approach):**
```
FLAG │ Header │ Data (stuffed) │ CRC │ FLAG
```

##### B3. Bit Stuffing
- Used in **HDLC** protocol.
- FLAG pattern = `01111110`
- After every **5 consecutive 1s** in data, sender inserts a **0 bit**.
- Receiver: after 5 consecutive 1s, if next bit is 0 → remove it; if 1 → it's a FLAG.

```
Data (original):   0 1 1 1 1 1 1 0
After stuffing:    0 1 1 1 1 1 0 1 0
                               ↑
                         Stuffed 0 (inserted after 5 ones)
```

**Interview Tip:**
> Bit stuffing is used by HDLC; byte stuffing by PPP.
> In bit stuffing, a 0 is inserted after five consecutive 1s.

#### Comparison Table

| Method | Delimiter | Problem | Used In |
|--------|-----------|---------|---------|
| Fixed-Size | None (implicit) | Padding waste | ATM |
| Character Count | Length field | Corrupted count → desync | Early protocols |
| Byte Stuffing | FLAG byte + ESC | ESC overhead | PPP |
| Bit Stuffing | `01111110` flag | Overhead for dense 1s | HDLC |

---

## 5. Frame Structure (Generic)

```
┌──────────┬──────────┬──────────┬──────────────────┬──────────┬──────────┐
│  Preamble│  Dest    │  Source  │  Type/Length     │  Data    │  FCS     │
│  (sync)  │  MAC     │  MAC     │  (Protocol type) │ (Payload)│ (CRC-32) │
└──────────┴──────────┴──────────┴──────────────────┴──────────┴──────────┘
```

| Field | Size | Purpose |
|-------|------|---------|
| Preamble | 7 bytes | Sync clocks (alternating 1s and 0s) |
| SFD (Start Frame Delimiter) | 1 byte | `10101011` — marks frame start |
| Dest MAC | 6 bytes | Target hardware address |
| Src MAC | 6 bytes | Sender hardware address |
| Type/Length | 2 bytes | Protocol type (IPv4=0x0800) or length |
| Data | 46–1500 bytes | Payload |
| FCS | 4 bytes | Frame Check Sequence (CRC-32 error detection) |

---

## 6. Interview Questions

**Q1: What is the main purpose of the Data Link Layer?**
> Ensure reliable hop-to-hop delivery of frames over a single physical link, including framing, MAC addressing, error detection, and access control.

**Q2: Difference between LLC and MAC sub-layers?**
> LLC (Logical Link Control) handles error/flow control and interfaces with the Network layer. MAC (Media Access Control) handles framing, physical addressing, and channel access.

**Q3: What is bit stuffing and why is it needed?**
> Bit stuffing inserts a `0` after five consecutive `1`s in the data to prevent the data from accidentally matching the FLAG pattern `01111110`, which marks frame boundaries in HDLC.

**Q4: What is the problem with Character Count framing?**
> If the count field gets corrupted during transmission, the receiver loses synchronization and cannot find where subsequent frames begin — a fatal and difficult-to-recover error.

**Q5: What is flow control at DLL?**
> Flow control prevents a fast sender from overwhelming a slow receiver. Stop-and-Wait allows one frame in flight at a time; Sliding Window allows multiple frames.

---

*Next: [02 — Error Detection & Correction →](./02_Error_Detection_and_Correction.md)*
