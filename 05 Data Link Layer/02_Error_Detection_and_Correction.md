# 🔍 Error Detection & Correction

> **⭐ HIGH PRIORITY TOPIC** — Almost guaranteed in interviews!

---

## 1. Why Error Detection?

Physical media is **imperfect** — electromagnetic noise, signal attenuation, and interference can flip bits during transmission. The Data Link Layer must detect (and sometimes correct) these errors.

```
Sender transmits: 1 0 1 1 0 1 0 0
                      ↕ (bit flip due to noise)
Receiver gets:    1 0 0 1 0 1 0 0
                      ↑ ERROR!
```

### Types of Errors
| Error Type | Description | Example |
|-----------|-------------|---------|
| **Single-bit error** | Only 1 bit changed | `10110100` → `10100100` |
| **Burst error** | Consecutive bits changed | `10110100` → `10000000` |

> **Burst errors are more common** in real networks (e.g., due to electrical interference affecting a short time window).

---

## 2. Error Detection vs. Correction

| | Error Detection | Error Correction |
|--|----------------|-----------------|
| **What it does** | Only *detects* if an error occurred | Finds AND *fixes* the error |
| **What's needed** | Ask for retransmission (ARQ) | Extra redundant bits (FEC) |
| **Overhead** | Lower | Higher |
| **Used when** | Retransmission is cheap (wired) | Retransmission is expensive (wireless, satellite) |
| **Examples** | CRC, Checksum, Parity | Hamming Code, Reed-Solomon |

---

## 3. Parity Bit

### 3.1 Concept
Add **1 extra bit** (the parity bit) so that the total number of `1`s in the data + parity bit is either:
- **Even** → Even Parity
- **Odd** → Odd Parity

### 3.2 Even Parity Example

```
Data to send: 1 0 1 1 0 1 0
Count of 1s:  4  (already even)
Parity bit:   0  (add 0 to keep total even)
Transmitted:  1 0 1 1 0 1 0 | 0
                              ↑ parity bit
```

```
Data to send: 1 0 1 1 1 1 0
Count of 1s:  5  (odd)
Parity bit:   1  (add 1 to make total even = 6)
Transmitted:  1 0 1 1 1 1 0 | 1
```

### 3.3 Detection
```
Received: 1 0 1 1 0 1 0 | 0   → Count 1s = 4 (even) ✅ No error
Received: 1 0 1 1 0 1 1 | 0   → Count 1s = 5 (odd)  ❌ Error detected!
```

### 3.4 2D Parity (Two-Dimensional Parity)

A better version: arrange data in a grid and compute parity for each **row AND column**.

```
Data arranged in rows:
  1 0 1 1 │ Parity(row)
  0 1 0 1 │ Parity(row)
  1 0 1 0 │ Parity(row)
  ─────────
  Parity   ← Column parities
  (col)

After computing:
  1 0 1 1 │ 1   (3 ones → add 1)
  0 1 0 1 │ 0   (2 ones → add 0)
  1 0 1 0 │ 0   (2 ones → add 0)
  ─────────
  0 1 0 0 │ 1   ← row of column parities
```

**Advantage**: Can **detect AND locate** a single-bit error (the erroneous row and column intersect at the bad bit) → enables correction!

### 3.5 Limitations of Simple Parity

| Detects | Misses |
|---------|--------|
| Any **odd** number of bit errors | Any **even** number of bit errors |
| Single-bit errors | 2-bit errors cancel each other out |

**Example of failure**:
```
Sent:     1 0 1 1 0 1 0 | 0  (parity=0, 4 ones)
2 bits flip:
Received: 1 1 1 0 0 1 0 | 0  (still 4 ones!) → Undetected error ❌
```

---

## 4. ⭐ CRC — Cyclic Redundancy Check (MOST IMPORTANT)

> **CRC is the most widely used error detection technique.** It is used in Ethernet, WiFi, USB, ZIP, and nearly all storage/networking protocols.

### 4.1 Core Concept

CRC treats the data as a **very large binary number** (dividend) and divides it by a **predetermined polynomial** (divisor). The **remainder** of this division is the CRC checksum, which is appended to the data. The receiver performs the same division and checks if the remainder is **zero**.

```
Sender:
  Data (M) ÷ Generator (G) = Quotient ... Remainder (R)
  Transmit: [M][R]  ← data + CRC remainder

Receiver:
  [M][R] ÷ G = 0 ?
  If remainder = 0 → ✅ No error
  If remainder ≠ 0 → ❌ Error detected
```

### 4.2 The Polynomial

A generator polynomial like `x³ + x + 1` is written as:
```
x³ + x + 1  ←→  binary: 1011
              (1 for x³, 0 for x², 1 for x, 1 for constant)
```

**Common CRC standards:**
| Standard | Polynomial | Bits | Used In |
|----------|-----------|------|---------|
| CRC-8 | `x⁸+x²+x+1` | 8 | ATM, Bluetooth |
| CRC-16 | `x¹⁶+x¹⁵+x²+1` | 16 | USB, ANSI |
| **CRC-32** | `x³²+x²⁶+...+1` | 32 | **Ethernet, ZIP, PNG** |
| CRC-CCITT | `x¹⁶+x¹²+x⁵+1` | 16 | HDLC, X.25 |

### 4.3 Step-by-Step CRC Calculation (MUST KNOW)

**Given:**
- Data (M) = `1011001`
- Generator (G) = `1011` (represents x³ + x + 1)
- Generator has **4 bits**, so we append **3 zeros** (degree of G = 3)

#### Step 1: Append zeros to data
```
Data with appended zeros = 1011001 000
                                   ↑↑↑
                             3 zeros appended (degree of generator)
```

#### Step 2: Perform Binary Division (XOR Division)
```
Key Rule: Subtract using XOR (no borrows; 1⊕1=0, 0⊕0=0, 1⊕0=1)

   1011001000   ÷   1011
 
Let me redo cleanly with alignment:

Dividend: 1 0 1 1 0 0 1 0 0 0
Divisor:  1 0 1 1

  1011001000
  1011
  ─────
  00000         (bring down 0)
  00001         (bring down 0)
  00010         (bring down 0)
  00100         (bring down 0)
  01000         (bring down 0)
  
  1000
  1011
  ──────
  0011  ← REMAINDER = 011 (3 bits = degree of generator)
```

> **Remainder = 011**

#### Step 3: Append CRC to original data
```
Transmitted frame = Data + Remainder = 1011001 011
```

#### Step 4: Receiver checks
```
Received: 1011001011
Divide by generator (1011):
  If remainder = 000 → ✅ No error
  If remainder ≠ 000 → ❌ Error!
```

### 4.4 Properties of CRC

| Property | Description |
|----------|-------------|
| Detects all **single-bit** errors | ✅ Always |
| Detects all **burst errors** of length ≤ degree(G) | ✅ Always |
| Detects most burst errors longer than degree(G) | ✅ With high probability |
| Detects all **odd** number of errors | ✅ If G has (x+1) as factor |
| Can it **correct** errors? | ❌ No (detection only) |

### 4.5 Why XOR Division?

In binary, XOR replaces subtraction:
```
1 ⊕ 1 = 0   (same as 1 - 1 = 0)
1 ⊕ 0 = 1   (same as 1 - 0 = 1)
0 ⊕ 1 = 1   (same as 0 - 1 with borrow = 1, ignore borrow)
0 ⊕ 0 = 0
```
XOR makes the math work in **GF(2)** (Galois Field of 2 elements) — no carries or borrows, just clean mod-2 arithmetic.

### 4.6 CRC Quick Summary

```
SENDER:
  1. Append (n) zeros to data M, where n = degree of generator G
  2. Divide M·2ⁿ by G using XOR division
  3. Get remainder R
  4. Transmit M + R

RECEIVER:
  1. Receive frame (M + R)
  2. Divide by G using XOR division
  3. If remainder = 0 → ✅ Accept
  4. If remainder ≠ 0 → ❌ Discard / request retransmission
```

---

## 5. Checksum

### 5.1 Concept

Checksum is used extensively at the **Transport and Network layers** (TCP, UDP, IP) but also appears in some DLL implementations.

The idea: **add all data segments** together, and send the **1's complement** of the sum as the checksum. The receiver adds all segments including the checksum — the result should be all 1s.

### 5.2 Sender Steps (1's Complement Checksum)

**Example:**
```
Data to send (two 8-bit segments):
  Segment 1:  10011010
  Segment 2:  01100110

Step 1: Add segments (binary addition)
  10011010
+ 01100110
──────────
 100000000   ← 9 bits (overflow/carry!)

Step 2: Wrap-around carry (add carry to LSB)
  00000000
+        1
──────────
  00000001

Step 3: Take 1's complement (flip all bits)
  11111110  ← This is the CHECKSUM

Step 4: Transmit:
  Segment 1 + Segment 2 + Checksum
  = 10011010 + 01100110 + 11111110
```

### 5.3 Receiver Steps

```
Receive: 10011010 + 01100110 + 11111110

Add all three:
  10011010
  01100110
  11111110
──────────
 111111110   ← overflow

Wrap-around:
  11111110
+        1
──────────
  11111111  ← All 1s!

Take 1's complement: 00000000

If result = 0 (all zeros after complement) → ✅ No error
If result ≠ 0 → ❌ Error detected
```

### 5.4 Limitations of Checksum

| Weakness | Explanation |
|---------|-------------|
| Cannot detect all errors | If two errors cancel each other out in the sum |
| Order-independent | Swapped segments may still produce valid checksum |
| Weaker than CRC | CRC has much better error detection capability |

### 5.5 Where Checksum is Used

| Protocol | Layer | Type |
|---------|-------|------|
| **IP** | Network | 16-bit 1's complement |
| **TCP** | Transport | 16-bit 1's complement |
| **UDP** | Transport | 16-bit 1's complement |
| **ICMP** | Network | 16-bit 1's complement |

---

## 6. Comparison: All Three Methods

| Feature | Parity | CRC | Checksum |
|---------|--------|-----|----------|
| **Technique** | Bit count | Polynomial division | Arithmetic sum |
| **Layer** | DLL | DLL | Network/Transport |
| **Error detection** | Single-bit only | Burst errors | General errors |
| **Overhead** | 1 bit | 8–32 bits | 8–16 bits |
| **Detects burst errors** | ❌ Weak | ✅ Excellent | ❌ Weak |
| **Error correction** | ❌ No (only 2D) | ❌ No | ❌ No |
| **Complexity** | Very Low | Medium | Low |
| **Common usage** | RAM parity | Ethernet, WiFi, USB | IP, TCP, UDP |

---

## 7. Error Correction — Hamming Code (Bonus)

> While usually asked at higher levels, good to know for completeness.

**Hamming Code** adds redundant bits at positions that are powers of 2 (1, 2, 4, 8, ...) to enable **single-bit error correction** and **double-bit error detection** (SECDED variant).

**Rule**: For `m` data bits, you need `r` parity bits such that: `2^r ≥ m + r + 1`

```
For 4 data bits: 2^r ≥ 4 + r + 1
  r=3: 2³=8 ≥ 4+3+1=8 ✅

Positions: 1  2  3  4  5  6  7
           P1 P2 D1 P3 D2 D3 D4
           ↑  ↑     ↑
           parity positions (powers of 2)
```

---

## 8. Interview Questions

**Q1: What is CRC? How does it work?**
> CRC appends a remainder (from polynomial XOR division of data by a generator) to the data. The receiver divides the received data+CRC by the same generator — a zero remainder means no error.

**Q2: Why do we append zeros before dividing in CRC?**
> Appending `n` zeros (where `n` = degree of generator) shifts the data left by `n` bit positions, making room for the CRC remainder to be attached at the end.

**Q3: What errors can CRC detect?**
> All single-bit errors, all burst errors of length ≤ degree(G), and all burst errors of odd length (if G has `x+1` as a factor).

**Q4: How does checksum differ from CRC?**
> Checksum uses arithmetic addition and 1's complement — simple but weaker. CRC uses polynomial XOR division — more complex but far better at detecting burst errors.

**Q5: Can CRC correct errors?**
> No, CRC only detects errors. Error correction requires more redundant information, like Hamming Code uses.

**Q6: What is the main limitation of the simple parity bit?**
> It cannot detect an even number of bit errors, as the errors cancel each other out in the parity count.

**Q7: What is 2D parity and why is it better?**
> 2D parity arranges data in a matrix and computes parity for each row and column. This allows detection AND correction of single-bit errors by identifying the exact row and column of the error.

---

*Next: [03 — MAC Address & Ethernet →](./03_MAC_Address_and_Ethernet.md)*
