# 📶 Multiple Access Protocols — ALOHA & CSMA/CD

> **Problem**: Multiple devices share a single broadcast channel. How do they coordinate transmission to avoid collisions?

---

## 1. The Multiple Access Problem

In a shared medium (e.g., a bus network, Wi-Fi), when **two or more devices transmit simultaneously**, their signals **collide and become garbled** — all transmissions are lost.

```
Device A ────────────────→ Signal A
                   ↕ COLLISION at the shared medium!
Device B ────────────────→ Signal B
                   ↓
           Signal A + Signal B = Garbage
```

Multiple Access Protocols control **who gets to transmit when** on a shared channel.

---

## 2. Categories of Multiple Access Protocols

```
Multiple Access Protocols
├── Channel Partitioning      (Divide channel into pieces)
│   ├── TDMA (Time Division)
│   ├── FDMA (Frequency Division)
│   └── CDMA (Code Division)
│
├── Random Access             ← Our Focus
│   ├── ALOHA (Pure & Slotted)
│   └── CSMA/CD (Ethernet)
│
└── Controlled Access
    ├── Token Ring
    ├── Polling
    └── Reservation
```

---

## 3. ALOHA Protocol

### 3.1 Background

ALOHA was developed at the **University of Hawaii in the 1970s** for wireless packet transmission between islands. It is the **ancestor of all random access protocols**.

Key idea: **Send whenever you have data. If collision → wait and retry.**

---

### 3.2 Pure ALOHA

#### Principle
- A node can **transmit a frame at any time** without checking the channel.
- If a **collision** occurs (ACK not received within timeout) → **wait a random time** and retransmit.
- Random backoff prevents repeated collisions.

```
Pure ALOHA Timeline:
Time ─────────────────────────────────────────────────────→

A: ████████            ████████
B:      ████████
         ↕ collision here!
                       ↑ A retransmits after random wait
```

#### Vulnerability Period

A frame is **at risk of collision** for an interval of **2 × frame transmission time (T)**:

```
Frame sent at time t → stays in channel from t to t+T
A collision occurs if anyone starts transmitting during [t-T, t+T]

Vulnerability window = 2T
```

This is because:
- A frame sent at `t−T` would overlap with our frame (arrives just as we start).
- A frame sent at `t+T` would overlap with our frame (starts just as we finish).

#### Efficiency (Throughput)

Let `G` = offered load (average number of transmission attempts per frame time).

$$S = G \cdot e^{-2G}$$

Maximum throughput achieved at `G = 0.5`:
$$S_{max} = \frac{1}{2e} \approx 0.184 \approx \textbf{18.4\%}$$

> Only **18.4% of channel capacity** is usefully used! Very inefficient.

---

### 3.3 Slotted ALOHA

#### Improvement Over Pure ALOHA
- **Time is divided into discrete slots** (each slot = one frame transmission time T).
- Nodes can **only begin transmission at the start of a slot** — never in the middle.
- This halves the vulnerability window!

```
Slotted ALOHA Timeline:
│ Slot │ Slot │ Slot │ Slot │ Slot │ Slot │
│  1   │  2   │  3   │  4   │  5   │  6   │
─────────────────────────────────────────────→

A:     │██████│      │      │██████│      │
B:     │      │██████│      │      │      │
C:     │      │      │██████│      │      │
```

#### Vulnerability Period

Since transmission can only START at slot boundaries:
- A collision only happens if **two nodes transmit in the same slot**.
- Vulnerability window = **T** (half that of Pure ALOHA!)

#### Efficiency

$$S = G \cdot e^{-G}$$

Maximum throughput achieved at `G = 1`:
$$S_{max} = \frac{1}{e} \approx 0.368 \approx \textbf{36.8\%}$$

> Slotted ALOHA achieves **double** the throughput of Pure ALOHA!

---

### 3.4 ALOHA Comparison Table

| Feature | Pure ALOHA | Slotted ALOHA |
|---------|-----------|--------------|
| **Transmission time** | Anytime | Start of slot only |
| **Vulnerability window** | 2T | T |
| **Efficiency formula** | $G e^{-2G}$ | $G e^{-G}$ |
| **Max efficiency** | **18.4%** (at G=0.5) | **36.8%** (at G=1) |
| **Synchronization** | Not needed | Requires time sync |
| **Collision probability** | Higher | Lower |

---

### 3.5 ALOHA — How Collision is Detected

In ALOHA:
- Sender **doesn't detect** collision during transmission.
- Instead, it **waits for an ACK** from the receiver.
- If no ACK received within timeout → **assume collision** → wait random time → retransmit.

---

## 4. CSMA/CD — Carrier Sense Multiple Access with Collision Detection

> **Used in Ethernet (IEEE 802.3)** — the most important multiple access protocol!

### 4.1 The Key Idea

CSMA/CD improves on ALOHA by adding:
1. **Carrier Sense (CS)**: Listen before you transmit.
2. **Collision Detection (CD)**: While transmitting, keep listening. If collision detected → stop immediately and send a jam signal.

```
ALOHA: "Transmit whenever, deal with collision later"
CSMA:  "Sense the channel first, only transmit if idle"
CSMA/CD: "Sense first + detect collision while transmitting + abort fast"
```

### 4.2 CSMA/CD Algorithm — Step by Step

```
┌─────────────────────────────────────────────────────────────┐
│                   CSMA/CD Algorithm                         │
└─────────────────────────────────────────────────────────────┘

1. Node wants to transmit a frame.

2. SENSE the channel:
   ├── Channel BUSY → WAIT until idle, then go to step 2
   └── Channel IDLE → Begin transmitting frame

3. While transmitting, MONITOR for collision:
   ├── No collision → Frame sent successfully ✅ Done
   └── COLLISION DETECTED:
         a. Immediately STOP transmission
         b. Send a JAM SIGNAL (48 bits) to notify all nodes
         c. BACKOFF: Wait random time using Binary Exponential Backoff
         d. Return to Step 2 (try again)

4. After too many retries (typically 16) → give up, report error
```

#### Visual Timeline
```
A: ██████████████████──────── (transmitting, no collision)

B starts before A finishes (doesn't sense A yet due to propagation delay):
A: ████████████ STOP | JAM   (collision detected, sends jam)
B:     ████████ STOP | JAM   (B also detects collision, stops)
        ↑ Collision!
        ↓
A waits random backoff time ─→ Retransmits ████████████████ ✅
```

### 4.3 Jam Signal

- **48 bits** of alternating 1s and 0s.
- Sent immediately after collision detection.
- Purpose: Ensure all other nodes **also detect the collision** (propagation delay means some may not have noticed yet).

```
Why 48 bits? 
The jam signal must propagate to all ends of the Ethernet segment.
48 bits at 10 Mbps = 4.8 µs — enough time for the signal to travel the full cable length.
```

### 4.4 Binary Exponential Backoff (BEB)

After a collision, each node waits a **random number of slot times** before retrying.

- After **1st collision**: Wait 0 or 1 slot times → `K ∈ {0, 1}`
- After **2nd collision**: Wait 0, 1, 2, or 3 slot times → `K ∈ {0, 1, 2, 3}`
- After **nth collision**: `K ∈ {0, 1, 2, ..., 2^n - 1}` (max = 1023)
- After **16 collisions**: Give up, report error.

$$\text{Wait} = K \times 51.2 \text{ µs} \quad \text{where} \quad K \in \{0, 1, ..., 2^{\min(n, 10)} - 1\}$$

**Example:**
```
1st collision: K ∈ {0, 1}         → wait 0 or 51.2 µs
2nd collision: K ∈ {0, 1, 2, 3}   → wait up to 153.6 µs
10th collision: K ∈ {0, ..., 1023} → wait up to 52.4 ms
16th collision: Abort!
```

> The backoff window **doubles** after each collision — hence "exponential". This reduces the probability of repeated collisions between the same nodes.

### 4.5 Why CSMA/CD Is Better Than Pure ALOHA

| Feature | Pure ALOHA | CSMA/CD |
|---------|-----------|---------|
| Check channel first? | ❌ No | ✅ Yes (Carrier Sense) |
| Stop on collision? | ❌ No (full frame sent) | ✅ Yes (abort immediately) |
| Efficiency | ~18.4% | Up to ~99% under low load |
| Channel wastage | High (entire frame wasted) | Low (only partial frame wasted) |

### 4.6 CSMA/CD Limitations

1. **Cannot be used for wireless (Wi-Fi)**:
   - Due to the **hidden node problem** and signal attenuation, a node can't reliably detect collisions on wireless medium.
   - Wi-Fi uses **CSMA/CA** (Collision Avoidance) instead.

2. **Not used in modern Ethernet**:
   - Modern Ethernet uses **full-duplex switches** with point-to-point links between device and switch.
   - No shared medium → no collisions possible → CSMA/CD is irrelevant.
   - But CSMA/CD is still conceptually important and tested in exams!

### 4.7 CSMA Persistence Strategies

Before transmitting, what should a node do when it finds the channel busy?

| Strategy | Behavior | Pros/Cons |
|---------|----------|-----------|
| **1-persistent** | Wait for channel to go idle, then transmit immediately | Simple; high collision probability |
| **Non-persistent** | Wait random time if busy, check again | Low collision; low efficiency |
| **p-persistent** | When idle: transmit with probability p, wait with probability (1-p) | Balance between collisions and efficiency |

**CSMA/CD uses 1-persistent** (for Ethernet).

---

## 5. CSMA/CA — Collision Avoidance (Bonus: Wi-Fi)

Used in **IEEE 802.11 (Wi-Fi)**. Since wireless can't detect collisions:

1. **DIFS**: Wait for DIFS (DCF Interframe Space) after channel goes idle.
2. **Backoff**: Start random backoff timer; count down only while channel is idle.
3. **Transmit** when timer reaches zero.
4. Wait for **ACK**; if no ACK → collision assumed → retry.

```
Wi-Fi CSMA/CA:
Channel: ──busy──│   DIFS   │countdown│──TX──│ACK│
```

---

## 6. Full Protocol Comparison

| Protocol | Category | Check before send? | Detect collision? | Max Efficiency |
|---------|---------|-------------------|-----------------|----------------|
| **Pure ALOHA** | Random | ❌ | ❌ | **18.4%** |
| **Slotted ALOHA** | Random | ❌ | ❌ | **36.8%** |
| **CSMA (no CD)** | Random | ✅ | ❌ | Better than ALOHA |
| **CSMA/CD** | Random | ✅ | ✅ | **High (~100% low load)** |
| **CSMA/CA** | Random | ✅ | ❌ (avoidance) | Good for wireless |
| **TDMA** | Partitioning | N/A | N/A | 100% (no collision) but wasted when idle |
| **Token Ring** | Controlled | N/A | N/A | High, no collision |

---

## 7. Interview Questions

**Q1: What is the difference between Pure ALOHA and Slotted ALOHA?**
> Pure ALOHA allows transmission at any time (vulnerability window = 2T, efficiency ≈ 18.4%). Slotted ALOHA restricts transmission to the start of time slots (vulnerability window = T, efficiency ≈ 36.8%).

**Q2: Why is Slotted ALOHA more efficient than Pure ALOHA?**
> By synchronizing transmissions to slot boundaries, the vulnerability window is halved (from 2T to T), reducing collision probability and doubling maximum throughput.

**Q3: Explain CSMA/CD step by step.**
> 1) Sense the channel — if busy, wait; if idle, transmit. 2) While transmitting, monitor for collision. 3) If collision detected, immediately stop and send a 48-bit jam signal. 4) Apply Binary Exponential Backoff — wait a random number of slot times. 5) Retry. After 16 failed attempts, abort.

**Q4: What is the purpose of the jam signal in CSMA/CD?**
> The jam signal (48 bits) is sent after a collision is detected to ensure all nodes on the segment are aware that a collision occurred, even those that may not have detected it yet due to propagation delay.

**Q5: What is Binary Exponential Backoff?**
> After the nth collision, a node waits a random time K × 51.2 µs where K is chosen from {0, 1, ..., 2^min(n,10) − 1}. The range doubles with each collision, reducing repeated collision probability.

**Q6: Why doesn't Wi-Fi use CSMA/CD?**
> In wireless, a node cannot simultaneously transmit and listen for collisions due to signal attenuation and the hidden node problem. Wi-Fi uses CSMA/CA (Collision Avoidance) instead.

**Q7: What is the hidden node problem?**
> Node A and C cannot hear each other (out of range), but both can hear node B. A and C might transmit simultaneously (both thinking channel is free), causing collision at B that neither can detect.

**Q8: Maximum efficiency of Pure ALOHA?**
> 18.4% = 1/(2e), achieved at load G = 0.5.

**Q9: Maximum efficiency of Slotted ALOHA?**
> 36.8% = 1/e, achieved at load G = 1.

---

*Next: [05 — Switching Basics →](./05_Switching_Basics.md)*
