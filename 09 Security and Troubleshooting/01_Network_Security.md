# Network Security

> Security is not a single feature — it's a set of **goals** achieved through **cryptographic tools** layered over the network stack.

---

## 1. Basics of Network Security

### 1.1 Security Goals (CIA Triad + 2 more)

```
┌─────────────────────────────────────────────────────────────┐
│                  The Security Goals                         │
│                                                             │
│  C  — CONFIDENTIALITY  Keep data secret from eavesdroppers  │
│  I  — INTEGRITY        Detect if data was tampered with     │
│  A  — AVAILABILITY     Services remain accessible           │
│  +  — AUTHENTICATION   Prove who you are                   │
│  +  — NON-REPUDIATION  Can't deny sending a message        │
└─────────────────────────────────────────────────────────────┘
```

| Goal | Question | Tool |
|------|---------|------|
| **Confidentiality** | Can others read it? | Encryption (AES, RSA) |
| **Integrity** | Was it modified? | Hash functions, MACs, Digital Signatures |
| **Availability** | Is it accessible? | Anti-DDoS, redundancy |
| **Authentication** | Who are you? | Passwords, certificates, MFA |
| **Non-repudiation** | Can they deny it? | Digital signatures |

### 1.2 The Threat Landscape

```
Threats to a Network:

Passive Attacks (eavesdrop — hard to detect):
  • Packet sniffing / eavesdropping
  • Traffic analysis (who talks to whom, how often)

Active Attacks (modify/disrupt — detectable):
  • Man-in-the-Middle (MITM)
  • Replay attacks
  • Denial of Service (DoS/DDoS)
  • IP Spoofing
  • DNS Poisoning / ARP Spoofing
  • Session Hijacking
```

---

## 2. Cryptography Fundamentals

### 2.1 What is Cryptography?

**Cryptography** is the science of securing communication by transforming readable data (**plaintext**) into an unreadable form (**ciphertext**) that can only be reversed by authorized parties.

```
Plaintext:  "HELLO"
    ↓  Encrypt (key)
Ciphertext: "KHOOR"   ← meaningless to eavesdropper
    ↓  Decrypt (key)
Plaintext:  "HELLO"   ← only authorized receiver can read
```

### 2.2 Types of Cryptography

```
Cryptography
├── Symmetric   — Same key to encrypt AND decrypt
├── Asymmetric  — Different keys: public key encrypts, private key decrypts
└── Hash        — One-way function, no decryption (fingerprint)
```

---

## 3. Symmetric Encryption

### 3.1 How It Works

**One shared secret key** is used for both encryption and decryption. Both parties must know the key in advance.

```
Sender                           Receiver
  │                                 │
  │  Key: "mysecret"                │  Key: "mysecret"
  │                                 │
  │  Plaintext: "Hello"             │
  │      ↓ Encrypt(key)             │
  │  Ciphertext: "XG7#k"  ────────→│
  │                                 │  Ciphertext: "XG7#k"
  │                                 │      ↓ Decrypt(key)
  │                                 │  Plaintext: "Hello" ✅
```

### 3.2 DES — Data Encryption Standard

```
Key size:    56 bits
Block size:  64 bits
Rounds:      16 Feistel rounds
Status:      ⚠️ BROKEN (1999) — too short key, cracked in 22 hours
```

**Why DES is broken:**
- 56-bit key → only 2⁵⁶ ≈ 72 quadrillion possible keys
- Modern hardware can brute-force this

**3DES (Triple DES):**
- Applies DES three times: Encrypt(K1) → Decrypt(K2) → Encrypt(K3)
- Effective key: 112 bits
- Slow; largely replaced by AES

### 3.3 AES — Advanced Encryption Standard ⭐

```
Key sizes:   128, 192, or 256 bits
Block size:  128 bits
Rounds:      10 (128-bit), 12 (192-bit), 14 (256-bit)
Status:      ✅ Current standard — widely used
```

**AES Internal Structure (simplified):**
```
Each round performs 4 operations on a 4×4 matrix of bytes (state):
  1. SubBytes    — Non-linear substitution using S-box
  2. ShiftRows   — Rotate rows of the state matrix
  3. MixColumns  — Mix each column (linear transformation)
  4. AddRoundKey — XOR state with round key derived from master key
```

**Where AES is used:**
- HTTPS (TLS) — AES-128 or AES-256
- WiFi (WPA2/WPA3) — AES-CCMP
- Full-disk encryption (BitLocker, FileVault)
- SSH, VPNs, file encryption

### 3.4 AES Modes of Operation

| Mode | Name | Description | Use Case |
|------|------|-------------|---------|
| **ECB** | Electronic Codebook | Each block encrypted independently | ❌ Avoid — patterns visible |
| **CBC** | Cipher Block Chaining | Each block XORed with previous ciphertext | File encryption |
| **CTR** | Counter Mode | Block cipher → stream cipher via counter | Streaming |
| **GCM** | Galois/Counter Mode | Encryption + Authentication | **TLS, HTTPS (most common)** |

> **AES-GCM** is the most widely used mode today — it provides both encryption and integrity (AEAD = Authenticated Encryption with Associated Data).

### 3.5 Symmetric Encryption: Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| Very fast | Key distribution problem — how to share the key securely? |
| Efficient for large data | n users need n(n-1)/2 keys! (doesn't scale) |
| Strong security (AES-256) | Both parties must have key before communicating |

---

## 4. Asymmetric Encryption (Public Key Cryptography)

### 4.1 How It Works

Each party has a **key pair**:
- **Public key**: Shared openly with everyone
- **Private key**: Never shared, kept secret

```
Math property:
  Encrypt with PUBLIC key  → Only PRIVATE key can decrypt
  Encrypt with PRIVATE key → Only PUBLIC key can decrypt (used for signatures)
```

```
Sender                           Receiver
  │                                 │
  │  Receiver's PUBLIC key known    │  Receiver's PRIVATE key (secret)
  │                                 │
  │  Plaintext: "Hello"             │
  │      ↓ Encrypt(receiver's pub)  │
  │  Ciphertext: "XG7#k" ─────────→│
  │                                 │  Ciphertext: "XG7#k"
  │                                 │      ↓ Decrypt(receiver's private)
  │                                 │  Plaintext: "Hello" ✅

ONLY receiver can decrypt (only they have private key)
Eavesdropper has ciphertext + public key, still can't decrypt!
```

### 4.2 RSA — Rivest-Shamir-Adleman

```
Key sizes:   1024, 2048, 4096 bits (2048+ recommended today)
Security:    Based on hardness of factoring large prime numbers
Status:      ✅ Widely used, but being replaced by ECC
```

**RSA Mathematical Foundation:**

```
Key Generation:
  1. Choose two large primes: p and q
  2. n = p × q  (modulus, public)
  3. φ(n) = (p-1)(q-1)  (Euler's totient)
  4. Choose e: 1 < e < φ(n), gcd(e, φ(n)) = 1 (public exponent, often 65537)
  5. Find d: d × e ≡ 1 (mod φ(n))  (private exponent)

Public key:  (e, n)
Private key: (d, n)

Encryption:  C = M^e mod n
Decryption:  M = C^d mod n

Security:    Factoring n into p and q is computationally infeasible for large n
```

**Simple Example (educational, small numbers):**
```
p=5, q=11 → n=55, φ(n)=40
e=3 (public), d=27 (private, since 3×27=81=2×40+1)

Encrypt M=2: C = 2³ mod 55 = 8
Decrypt C=8: M = 8²⁷ mod 55 = 2 ✅
```

**Where RSA is used:**
- TLS/HTTPS handshake (exchanging symmetric keys)
- Digital signatures (emails, code signing)
- SSH authentication
- Certificate authorities

### 4.3 Asymmetric Encryption: Pros & Cons

| ✅ Pros | ❌ Cons |
|--------|--------|
| No key distribution problem | **Very slow** (1000x slower than AES) |
| Scales (1 key pair per person) | Large key sizes needed |
| Enables digital signatures | **NOT used for bulk data encryption** |
| Public key can be freely shared | Mathematical advances could break it |

> **In practice**: Use asymmetric crypto to **securely exchange a symmetric key** (key agreement), then use symmetric crypto (AES) for all actual data. This is exactly what TLS does!

---

## 5. Diffie-Hellman Key Exchange

### 5.1 The Key Distribution Problem

Symmetric encryption is fast, but how do two parties agree on a shared key **without ever having met** and without a trusted third party?

> If they send the key over an insecure channel, an attacker can intercept it!

### 5.2 The Brilliant Solution: Diffie-Hellman

DH allows two parties to **establish a shared secret over a public channel** — even if an attacker sees all messages, they can't compute the secret!

### 5.3 Analogy: Paint Mixing

```
1. Alice & Bob publicly agree on a base color: YELLOW

2. Alice picks secret color: RED (private)
   Alice mixes: YELLOW + RED = ORANGE → Sends ORANGE publicly

3. Bob picks secret color: BLUE (private)
   Bob mixes: YELLOW + BLUE = GREEN → Sends GREEN publicly

4. Alice takes Bob's GREEN + her secret RED:
   GREEN + RED = BROWN

5. Bob takes Alice's ORANGE + his secret BLUE:
   ORANGE + BLUE = BROWN ← Same color!

Attacker sees: YELLOW, ORANGE, GREEN — can't determine the shared BROWN
(can't "un-mix" colors to find the secret components!)
```

### 5.4 Mathematical DH

```
Public parameters (everyone knows):
  p = large prime number
  g = generator (primitive root mod p)

Alice's private: a (secret)
Bob's private:   b (secret)

Step 1: Alice computes: A = g^a mod p → sends A to Bob
Step 2: Bob computes:   B = g^b mod p → sends B to Alice

Step 3: Alice computes shared secret: s = B^a mod p = g^(ab) mod p
Step 4: Bob computes shared secret:   s = A^b mod p = g^(ab) mod p

Both get the same s = g^(ab) mod p ✅

Attacker sees: p, g, A (=g^a mod p), B (=g^b mod p)
To find s, they'd need to solve the Discrete Logarithm Problem
(given g^a mod p, find a) — computationally infeasible for large p!
```

**Example (small, educational):**
```
p=23, g=5
Alice: a=6 → A = 5⁶ mod 23 = 8   (sends 8)
Bob:   b=15 → B = 5¹⁵ mod 23 = 19 (sends 19)

Alice: s = 19⁶ mod 23 = 2
Bob:   s = 8¹⁵ mod 23 = 2  ← Both get 2! ✅
```

### 5.5 DH in Practice

- DH is used in **TLS** to establish session keys
- **ECDH (Elliptic Curve Diffie-Hellman)** is the modern version — much smaller keys, same security
- DH provides **Perfect Forward Secrecy (PFS)**: even if private keys are compromised later, past sessions remain secure (each session uses a fresh DH exchange)

---

## 6. Hash Functions

### 6.1 What is a Hash Function?

A **hash function** takes input of any size and produces a **fixed-size output (digest)** in a deterministic, one-way manner.

```
SHA-256("Hello World") = a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
SHA-256("hello World") = 0x3b6a...  (completely different — avalanche effect!)
                                     (one character change → totally new hash)
```

### 6.2 Properties of Cryptographic Hash Functions

| Property | Meaning |
|---------|---------|
| **Deterministic** | Same input → always same output |
| **One-way (pre-image resistance)** | Cannot reverse: given hash, can't find input |
| **Avalanche effect** | Tiny input change → completely different hash |
| **Collision resistance** | Hard to find two different inputs with same hash |
| **Fixed output size** | Input of any length → always same output length |

### 6.3 Common Hash Algorithms

| Algorithm | Output Size | Status |
|---------|------------|--------|
| **MD5** | 128 bits | ❌ Broken — collisions found |
| **SHA-1** | 160 bits | ❌ Deprecated — collisions found (2017) |
| **SHA-256** | 256 bits | ✅ Widely used, secure |
| **SHA-3** | Variable | ✅ Latest NIST standard |
| **bcrypt** | 184 bits | ✅ Best for passwords (slow by design) |

### 6.4 Uses of Hash Functions

| Use | How | Example |
|-----|-----|---------|
| **Data integrity** | Hash before/after transfer, compare | File downloads (checksums) |
| **Password storage** | Store hash(password), never plaintext | Linux /etc/shadow |
| **Digital signatures** | Sign hash(message) | Code signing, email |
| **HMAC** | Hash + secret key = authentication | TLS MAC |
| **Blockchain** | Chain of block hashes | Bitcoin |

### 6.5 Password Hashing

```
Wrong way (plain storage):
  DB: { username: "alice", password: "secret123" }
  ← If DB is compromised, all passwords exposed!

Correct way (hash + salt):
  salt = random value (e.g., "xK7j9m")
  stored = bcrypt(salt + "secret123")
  DB: { username: "alice", hash: "$2b$12$...", salt: "xK7j9m" }

Why salt? Prevents rainbow table attacks (precomputed hash tables)
```

---

## 7. Digital Signatures

### 7.1 What is a Digital Signature?

A **digital signature** proves:
1. **Authenticity** — the message came from the claimed sender
2. **Integrity** — the message was not altered
3. **Non-repudiation** — the sender cannot deny sending it

### 7.2 How Digital Signatures Work

```
SIGNING (Sender — Alice):
  1. Hash the message:       h = SHA-256(message)
  2. Encrypt hash with PRIVATE key:  signature = RSA_encrypt(h, Alice_private_key)
  3. Send: message + signature

VERIFYING (Receiver — Bob):
  1. Hash received message:  h' = SHA-256(received_message)
  2. Decrypt signature with Alice's PUBLIC key:  h = RSA_decrypt(signature, Alice_public_key)
  3. Compare: if h == h' → ✅ Valid signature (authentic + unmodified)
                         → ❌ Invalid (tampered or wrong sender)
```

### 7.3 Visual Diagram

```
Alice signs a document:
  [Message] ──SHA256──→ [Hash h]
                              ↓ Alice's Private Key
                        [Signature σ]

  Sends: [Message] + [Signature σ]

Bob verifies:
  [Message] ──SHA256──→ [Hash h']       Compare: h == h'?
  [Signature σ] ──Alice's Public Key──→ [Hash h]   ✅ or ❌
```

### 7.4 Digital Certificates (PKI)

How does Bob know the public key he has actually belongs to Alice?

**Certificate Authority (CA)** solves this:

```
CA (trusted third party) signs a certificate:
  Certificate = {
    Owner: "alice@example.com"
    Public Key: [Alice's public key]
    Validity: 2024-01-01 to 2025-01-01
    Signed by: GlobalSign CA (using CA's private key)
  }

Bob verifies:
  1. Gets Alice's certificate
  2. Verifies CA's signature using CA's public key (pre-installed in OS/browser)
  3. If valid → trusts that public key belongs to Alice ✅
```

---

## 8. SSL/TLS — Secure Communication

### 8.1 What is TLS?

**TLS (Transport Layer Security)** is the protocol that secures HTTPS, email, VPNs. It provides:
- **Confidentiality** → AES encryption of data
- **Integrity** → HMAC or AEAD ensures no tampering
- **Authentication** → Server (and optionally client) certificates

```
HTTP  + TLS = HTTPS
SMTP  + TLS = SMTPS
IMAP  + TLS = IMAPS
```

### 8.2 TLS Handshake (Simplified)

```
Client                                         Server
  │                                               │
  │── 1. ClientHello ───────────────────────────→│
  │   (TLS version, cipher suites, client_random) │
  │                                               │
  │←── 2. ServerHello ────────────────────────── │
  │   (chosen cipher, server_random, certificate) │
  │                                               │
  │   [Client verifies server's certificate       │
  │    using CA's public key]                     │
  │                                               │
  │── 3. Key Exchange ──────────────────────────→│
  │   (Diffie-Hellman public value or             │
  │    pre-master secret encrypted with           │
  │    server's public key)                       │
  │                                               │
  │   [Both compute same session keys             │
  │    from key exchange + randoms]               │
  │                                               │
  │── 4. Finished (encrypted) ─────────────────→ │
  │←── 4. Finished (encrypted) ────────────────── │
  │                                               │
  │══════ All data now encrypted (AES) ══════════ │
```

### 8.3 TLS Cipher Suite

A cipher suite specifies **which algorithms** are used for each task:

```
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256

  ECDHE      → Key Exchange (Elliptic Curve Diffie-Hellman Ephemeral)
  RSA        → Authentication (verify server's certificate)
  AES_128    → Bulk encryption (128-bit AES)
  GCM        → Mode (Galois/Counter Mode — provides AEAD)
  SHA256     → Message integrity (HMAC using SHA-256)
```

---

## 9. Common Network Attacks

### 9.1 MITM — Man-in-the-Middle Attack

**The attack:**
The attacker secretly **intercepts communication** between two parties, potentially reading or modifying all data.

```
Normal:  Alice ────────────────────── Bob
MITM:    Alice ──→ [ATTACKER] ──→ Bob
              ←─ [ATTACKER] ←──
Alice and Bob think they're talking to each other!
```

**Common MITM techniques:**

| Technique | How |
|-----------|-----|
| **ARP Spoofing** | Attacker sends fake ARP replies, poisoning ARP caches |
| **DNS Poisoning** | Fake DNS entries redirect to attacker's server |
| **SSL Stripping** | Downgrade HTTPS to HTTP (attacker in the middle) |
| **Evil Twin AP** | Fake WiFi hotspot that looks like legitimate one |
| **BGP Hijacking** | Announce false BGP routes to redirect internet traffic |

**MITM via ARP Spoofing example:**
```
Network: Alice (192.168.1.10), Router (192.168.1.1), Attacker (192.168.1.99)

Attacker sends to Alice:  "192.168.1.1 (router) is at ATTACKER_MAC"
Attacker sends to Router: "192.168.1.10 (Alice) is at ATTACKER_MAC"

Now:
  Alice → Router traffic → goes to Attacker first!
  Attacker reads/modifies → forwards to Router
  Router → Alice traffic → goes to Attacker first!
  ← Complete MITM ←
```

**Defenses against MITM:**
```
✅ HTTPS / TLS     — Encryption + server certificate verification
✅ Certificate Pinning — App only accepts specific certificates
✅ HSTS             — Browser forces HTTPS (no downgrade possible)
✅ Dynamic ARP Inspection (DAI) — Switch validates ARP packets
✅ DNSSEC           — Cryptographically signed DNS records
✅ VPN              — Encrypted tunnel bypasses local attacker
```

---

### 9.2 DDoS — Distributed Denial of Service

**The attack:**
Overwhelm a target (server, network) with **massive amounts of traffic** from **many sources simultaneously** (a botnet), making the service unavailable to legitimate users.

```
           Botnet (thousands of compromised machines)
           PC1, PC2, PC3, PC4, PC5, ..., PC10,000
              │    │    │    │    │
              └────┴────┴────┴────┘
                         │ millions of requests/sec
                         ↓
                    [Target Server]
                    CPU: 100%
                    Bandwidth: FULL
                    Legitimate users: ❌ Cannot connect!
```

**Types of DDoS Attacks:**

| Type | How | Layer |
|------|-----|-------|
| **Volumetric** | Flood bandwidth with UDP/ICMP traffic | L3/L4 |
| **TCP SYN Flood** | Send millions of SYN packets, never complete handshake | L4 |
| **HTTP Flood** | Legitimate-looking HTTP GET/POST requests at scale | L7 |
| **Amplification** | Small request → large response (DNS/NTP amplification) | L3 |
| **Slowloris** | Hold many connections open very slowly | L7 |

**SYN Flood in detail:**
```
Normal TCP Handshake:
  Client → Server: SYN
  Server → Client: SYN-ACK (server allocates resource!)
  Client → Server: ACK  (completes connection)

SYN Flood Attack:
  Attacker → Server: SYN (spoofed IP)
  Server → [ghost IP]: SYN-ACK (resource allocated, waits for ACK)
  ACK never comes! → Server's connection table fills up → Out of memory!

Defense: SYN Cookies — server encodes state in SYN-ACK itself, 
         allocates resources only AFTER valid ACK received
```

**DNS Amplification:**
```
Attacker (spoofed as victim 1.2.3.4) → DNS Server: "Give me ALL records for example.com"
DNS Server → 1.2.3.4 (victim): [Large response — 100× the request size]

Attacker sends 1 byte → victim gets 100 bytes
With thousands of DNS servers → victim overwhelmed!
```

**DDoS Defenses:**

```
✅ Rate Limiting          — Limit requests per IP per second
✅ CDN / Anycast          — Distribute attack across many PoPs globally
✅ Traffic Scrubbing      — DDoS mitigation provider filters malicious traffic
✅ BGP Blackholing        — Route attack traffic to null (affects good traffic too)
✅ SYN Cookies            — Stateless SYN flood protection
✅ CAPTCHA               — Distinguish bots from humans at app layer
✅ IP Reputation Lists    — Block known bad IPs
✅ Anycast DNS           — Distribute DNS queries to avoid DNS DDoS
```

---

## 10. Cryptography Comparison Table

| Aspect | Symmetric (AES) | Asymmetric (RSA) | Hash (SHA-256) |
|--------|:--------------:|:---------------:|:--------------:|
| **Keys** | 1 shared key | 2 keys (public + private) | No key |
| **Speed** | ✅ Fast | ❌ ~1000x slower | ✅ Fast |
| **Key size** | 128/256 bits | 2048/4096 bits | N/A |
| **Reversible** | ✅ Yes (decrypt) | ✅ Yes (with private key) | ❌ One-way |
| **Use case** | Bulk data encryption | Key exchange, signatures | Integrity, passwords |
| **Provides** | Confidentiality | Confidentiality, Auth | Integrity |
| **Example** | AES-256-GCM | RSA-2048, ECDH | SHA-256, bcrypt |

---

## 11. Interview Questions

**Q1: What is the difference between symmetric and asymmetric encryption?**
> Symmetric uses ONE shared key for both encryption and decryption (AES) — fast but requires secure key exchange. Asymmetric uses a KEY PAIR — public key encrypts, private key decrypts (RSA) — slow but solves key distribution. In practice, TLS uses asymmetric to exchange a symmetric key, then symmetric for all data.

**Q2: What is Diffie-Hellman key exchange?**
> DH allows two parties to establish a shared secret over an insecure channel without ever transmitting the secret. Based on the discrete logarithm problem: both parties exchange public values (g^a mod p, g^b mod p); each computes g^(ab) mod p as the shared secret. An eavesdropper cannot compute this from the public values alone.

**Q3: What is a hash function and what are its properties?**
> A hash function maps any input to a fixed-size output deterministically and irreversibly. Key properties: one-way (can't reverse), deterministic (same input = same output), collision resistant (can't find two inputs with same hash), avalanche effect (tiny change = completely different hash).

**Q4: What is a MITM attack and how is it prevented?**
> A Man-in-the-Middle attack intercepts communication between two parties (via ARP spoofing, DNS poisoning, rogue WiFi, etc.). Prevention: HTTPS with certificate verification (attacker can't fake a valid CA-signed cert), HSTS, DNSSEC, certificate pinning, and VPNs.

**Q5: What is a DDoS attack?**
> A Distributed Denial of Service attack floods a target with traffic from many compromised machines (botnet) to exhaust resources and make the service unavailable. Types include volumetric floods, SYN floods, HTTP floods, and amplification attacks. Defenses include rate limiting, CDNs, traffic scrubbing, and SYN cookies.

**Q6: What is the purpose of a digital signature?**
> A digital signature provides authenticity (message from claimed sender), integrity (not tampered), and non-repudiation (sender can't deny). Sender hashes the message, encrypts hash with their PRIVATE key → creates signature. Receiver decrypts with sender's PUBLIC key, recomputes hash, compares.

**Q7: How does TLS work at a high level?**
> TLS handshake: 1) Client and server agree on cipher suite. 2) Server sends certificate (verifies server identity). 3) Key exchange (DH) establishes a shared session key. 4) All subsequent data encrypted with AES using that session key. Provides confidentiality, integrity, and authentication.

**Q8: Why is MD5 no longer recommended for security?**
> MD5 collisions (two different inputs with same hash) can be computed in seconds on modern hardware. This allows attackers to forge certificates or create malicious files that have the same MD5 as legitimate ones. Use SHA-256 or SHA-3 instead.

---

*Next: [02 — Network Troubleshooting →](./02_Network_Troubleshooting.md)*
