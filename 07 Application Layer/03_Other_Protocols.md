# 📦 Other Application Layer Protocols — FTP, SMTP & DHCP

---

## 1. FTP — File Transfer Protocol

### 1.1 What is FTP?

**FTP (File Transfer Protocol)** is a standard protocol used to **transfer files** between a client and a server over a TCP/IP network. It's one of the oldest application layer protocols (RFC 959, 1985).

```
FTP Client (you)                     FTP Server (remote)
      │                                     │
      │─── Connect on port 21 ────────────→ │  (Control connection)
      │                                     │
      │─── Commands: USER, PASS, LIST, ──→  │
      │             RETR, STOR, QUIT        │
      │                                     │
      │←── Responses (code + message) ─────│
      │                                     │
      │════ Data connection (port 20) ══════│  (Data transfer)
      │         (file data flows here)      │
```

### 1.2 FTP's Dual-Connection Architecture ⭐

This is what makes FTP unique — it uses **TWO separate TCP connections**:

```
┌──────────────────────────────────────────────────────────────────┐
│  Control Connection (Port 21) — Persistent                      │
│  Used for: commands (USER, PASS, LIST, RETR, STOR) and          │
│            responses (150, 200, 221, 530...)                    │
│  Stays open for the entire FTP session                          │
├──────────────────────────────────────────────────────────────────┤
│  Data Connection (Port 20) — Created per transfer               │
│  Used for: actual file/directory listing data                   │
│  Created for each file transfer, then closed                    │
└──────────────────────────────────────────────────────────────────┘
```

### 1.3 Active vs Passive FTP ⭐ Common Interview Topic

#### Active Mode
The **server initiates** the data connection back to the client:

```
Client (random port > 1023)          Server (port 21)
  │─── PORT 55000 ─────────────────→ │  (client says: "connect to me on 55000")
  │                                   │
  │←── Server initiates data ─────── │  (server connects from port 20 to client:55000)
  │    connection from port 20        │

Problem: Client firewall often BLOCKS incoming connections from server!
```

#### Passive Mode
The **client initiates** both connections:

```
Client                               Server (port 21)
  │─── PASV ───────────────────────→ │  (client says: "give me a data port")
  │←── Server: "Use port 50021" ──── │
  │                                   │
  │─── Client connects to port 50021→ │  (client opens data connection)

Solution: Client initiates everything → works through firewalls!
```

| Feature | Active Mode | Passive Mode |
|---------|------------|--------------|
| Who opens data connection? | **Server** → Client | **Client** → Server |
| Data port (server side) | 20 | Random high port (PASV) |
| Firewall-friendly? | ❌ Client firewall blocks | ✅ Works through firewalls |
| Common use | Legacy | **Modern default** |

### 1.4 FTP Commands

| Command | Action |
|---------|--------|
| `USER <name>` | Send username |
| `PASS <password>` | Send password |
| `LIST` | List directory contents |
| `CWD <dir>` | Change working directory |
| `RETR <file>` | Retrieve (download) a file |
| `STOR <file>` | Store (upload) a file |
| `DELE <file>` | Delete a file |
| `QUIT` | Close the session |
| `PASV` | Enter passive mode |
| `PORT` | Enter active mode |

### 1.5 FTP Response Codes

| Code | Meaning |
|------|---------|
| 200 | Command OK |
| 220 | Service ready |
| 226 | Transfer complete |
| 230 | User logged in |
| 331 | Password required |
| 425 | Can't open data connection |
| 530 | Not logged in |
| 550 | File not found / permission denied |

### 1.6 FTP Security Issues

**FTP is completely insecure** — credentials and data are sent in **plain text**!

```
Wireshark capture of FTP session:
  220 FTP Server Ready
  USER alice
  331 Password required
  PASS mysecretpassword   ← PLAINTEXT PASSWORD! Anyone can see this!
  230 User logged in
```

**Secure Alternatives:**

| Protocol | Full Name | Security | Port |
|---------|-----------|---------|------|
| **SFTP** | SSH File Transfer Protocol | SSH-encrypted | 22 |
| **FTPS** | FTP over TLS/SSL | TLS-encrypted | 990 (implicit) / 21 (explicit) |
| **SCP** | Secure Copy Protocol | SSH-encrypted | 22 |

> **SFTP ≠ FTPS**: SFTP is a completely different protocol (part of SSH). FTPS is FTP with TLS encryption added.

### 1.7 FTP Modes: ASCII vs Binary

| Mode | Use | How it works |
|------|-----|-------------|
| **ASCII** | Text files (.txt, .html) | Converts line endings between OS formats |
| **Binary (Image)** | Everything else | Transfers raw bytes, no conversion |

> Always use **Binary mode** for non-text files to avoid corruption!

---

## 2. SMTP — Simple Mail Transfer Protocol

### 2.1 What is SMTP?

**SMTP (Simple Mail Transfer Protocol)** is the standard protocol for **sending and relaying email** between mail servers. It's a push protocol — SMTP pushes email to the recipient's server.

```
                    SMTP                   SMTP
Sender's Client ──────────→ Sender's  ──────────→ Recipient's
(Mail App)         send      Mail Server  relay     Mail Server
                             (outgoing)             (incoming)
                                                        │
                                                  POP3/IMAP
                                                        │
                                                Recipient's Client
                                                (reads email)
```

### 2.2 Email Protocol Overview

| Protocol | Direction | Purpose | Port |
|---------|-----------|---------|------|
| **SMTP** | Client → Server, Server → Server | **Sending** email | 25 (server-to-server), 587 (client-to-server) |
| **POP3** | Server → Client | **Downloading** email (removes from server) | 110 (plain), 995 (TLS) |
| **IMAP** | Server ↔ Client | **Syncing** email (stays on server) | 143 (plain), 993 (TLS) |

### 2.3 How Email Delivery Works — End to End

```
Step 1: Alice composes email to bob@example.com in Gmail (client)
Step 2: Gmail client connects to Gmail SMTP server (smtp.gmail.com:587)
        Alice authenticates and uploads the email
Step 3: Gmail SMTP server does DNS lookup for example.com's MX record
        "example.com MX → mail.example.com"
Step 4: Gmail SMTP server connects to mail.example.com port 25
        Delivers the email (SMTP relay)
Step 5: mail.example.com stores the email in Bob's mailbox
Step 6: Bob opens Outlook → connects to mail.example.com via IMAP/POP3
        Downloads/syncs the email
```

### 2.4 SMTP Session — Step by Step

```
Client                                        Server
  │                                               │
  │←── 220 smtp.gmail.com ESMTP ready ────────── │  Server greeting
  │                                               │
  │─── EHLO alice.com ─────────────────────────→ │  Client introduces itself
  │←── 250-smtp.gmail.com                        │  Server capabilities
  │    250-STARTTLS                               │
  │    250 AUTH LOGIN PLAIN                       │
  │                                               │
  │─── AUTH LOGIN ────────────────────────────→  │  Authenticate
  │←── 334 (base64 prompt)                        │
  │─── (base64 username)                          │
  │←── 334 (password prompt)                      │
  │─── (base64 password)                          │
  │←── 235 Authentication successful             │
  │                                               │
  │─── MAIL FROM: <alice@gmail.com> ──────────→  │  Envelope from
  │←── 250 OK                                    │
  │                                               │
  │─── RCPT TO: <bob@example.com> ────────────→  │  Envelope to
  │←── 250 OK                                    │
  │                                               │
  │─── DATA ──────────────────────────────────→  │  Start message body
  │←── 354 End data with <CR><LF>.<CR><LF>       │
  │─── From: alice@gmail.com                      │
  │    To: bob@example.com                        │
  │    Subject: Hello!                            │
  │                                               │
  │    Hi Bob, how are you?                       │
  │    .                                          │  Single dot ends message
  │←── 250 Message accepted                       │
  │                                               │
  │─── QUIT ──────────────────────────────────→  │
  │←── 221 Bye                                   │
```

### 2.5 SMTP Commands

| Command | Purpose |
|---------|---------|
| `EHLO / HELO` | Client identifies itself to server (EHLO = extended) |
| `MAIL FROM:` | Specifies sender's email address |
| `RCPT TO:` | Specifies recipient's email address |
| `DATA` | Start of message body |
| `.` (single dot) | Ends the message body |
| `QUIT` | Ends the SMTP session |
| `AUTH` | Authenticate with server |
| `STARTTLS` | Upgrade connection to TLS |

### 2.6 SMTP Response Codes

| Code | Meaning |
|------|---------|
| 220 | Service ready |
| 221 | Closing connection (goodbye) |
| 235 | Authentication successful |
| 250 | Command completed successfully |
| 354 | Start mail input |
| 421 | Service unavailable (try again) |
| 450 | Mailbox busy (try again) |
| 500 | Syntax error, command unrecognized |
| 530 | Authentication required |
| 550 | Mailbox unavailable / does not exist |

### 2.7 Email Headers

```
Received: from mail.gmail.com ([209.85.220.41])  ← Path it traveled
From: alice@gmail.com
To: bob@example.com
Subject: Hello Bob!
Date: Sat, 21 Jun 2025 10:21:25 +0000
Message-ID: <unique-id@gmail.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
```

### 2.8 Email Anti-Spam Mechanisms

| Mechanism | How It Works |
|-----------|-------------|
| **SPF** (Sender Policy Framework) | DNS TXT record lists IPs authorized to send for a domain |
| **DKIM** (DomainKeys Identified Mail) | Server signs email with private key; recipient verifies with public key from DNS |
| **DMARC** | Policy that says what to do if SPF/DKIM fail (quarantine/reject) |

### 2.9 POP3 vs IMAP

| Feature | POP3 | IMAP |
|---------|------|------|
| **Protocol** | Post Office Protocol v3 | Internet Message Access Protocol |
| **Port** | 110 (plain), 995 (TLS) | 143 (plain), 993 (TLS) |
| **How it works** | Downloads email to client, deletes from server | Syncs email; stays on server |
| **Multi-device** | ❌ Poor (email only on one device) | ✅ Great (sync across all devices) |
| **Offline access** | ✅ Yes (downloaded) | ✅ Yes (if cached) |
| **Storage** | Local | Server |
| **Use case** | Single device users | **Modern use (Gmail, Outlook)** |

---

## 3. DHCP — Dynamic Host Configuration Protocol

### 3.1 What is DHCP?

**DHCP** automatically assigns network configuration to devices when they connect to a network, so you don't have to manually configure IP, subnet, gateway, and DNS on every device.

**What DHCP assigns:**
```
✅ IP Address          (e.g., 192.168.1.100)
✅ Subnet Mask         (e.g., 255.255.255.0)
✅ Default Gateway     (e.g., 192.168.1.1)
✅ DNS Server(s)       (e.g., 8.8.8.8, 8.8.4.4)
✅ Lease Duration      (e.g., 24 hours)
```

### 3.2 DHCP Architecture

```
DHCP Client                            DHCP Server
(Your phone, laptop, etc.)             (Your router, or dedicated server)
        │                                      │
        │  Uses UDP port 68 (client)           │
        │  Server uses UDP port 67             │
        │                                      │
```

**DHCP uses UDP** (not TCP) because:
- The client has no IP yet — can't set up a TCP connection
- Broadcasts are used — TCP doesn't support broadcast
- If DHCP fails, just retry — no need for TCP's reliability overhead

### 3.3 The DORA Process ⭐ MUST KNOW

The DHCP lease acquisition has 4 steps: **D**iscover → **O**ffer → **R**equest → **A**cknowledge

```
Client                                          Server
  │                                               │
  │ 1. DHCP DISCOVER (broadcast)                  │
  │    Src: 0.0.0.0:68  Dst: 255.255.255.255:67  │
  │    "I need an IP! Is there a DHCP server?"    │
  │────────────────────────────────────────────→  │
  │                                               │
  │ 2. DHCP OFFER (broadcast or unicast)          │
  │←────────────────────────────────────────────  │
  │    "Here! Take 192.168.1.100, mask /24,       │
  │     gateway 192.168.1.1, lease 24hrs"         │
  │                                               │
  │ 3. DHCP REQUEST (broadcast)                   │
  │    "I'd like to accept 192.168.1.100"         │
  │    (broadcast so other servers know too)      │
  │────────────────────────────────────────────→  │
  │                                               │
  │ 4. DHCP ACKNOWLEDGE (broadcast or unicast)    │
  │←────────────────────────────────────────────  │
  │    "It's yours! Lease expires in 24 hours"    │
  │                                               │
  [Client configures its network stack]
```

> **Memory trick**: **D**ora the **E**xplorer = **D**iscover, **O**ffer, **R**equest, A**ck**

### 3.4 Why Broadcasts in DHCP?

| Step | Type | Reason |
|------|------|--------|
| **Discover** | Broadcast (`255.255.255.255`) | Client has no IP, doesn't know server's IP |
| **Offer** | Broadcast or Unicast | Client has no IP yet (can't receive unicast reliably) |
| **Request** | Broadcast | Multiple DHCP servers may have offered; broadcast declines others |
| **ACK** | Broadcast or Unicast | Client may not have IP configured yet |

### 3.5 DHCP Lease

A DHCP-assigned IP is a **lease** — not permanent. The server rents the IP for a fixed duration:

```
Lease Duration: 24 hours (86400 seconds)

Timeline:
T=0:       Client gets IP 192.168.1.100
T=12hrs:   Client sends DHCP Request to RENEW (at 50% of lease)
T=18hrs:   If no renewal, tries broadcast (at 87.5% of lease)
T=24hrs:   Lease expires! Client releases IP, must get new one
           (If still connected, it broadcasts DISCOVER again)
```

**DHCP RELEASE**: Client explicitly tells server "I'm done with this IP":
```
Client shuts down gracefully:
  Sends: DHCP RELEASE  (Src: 192.168.1.100, "I'm releasing this IP")
  Server frees 192.168.1.100 for others
```

### 3.6 DHCP Messages Summary

| Message | Sender | Direction | Purpose |
|---------|--------|-----------|---------|
| **DISCOVER** | Client | Broadcast | "Anyone there? I need an IP" |
| **OFFER** | Server | Broadcast/Unicast | "Here's an available IP" |
| **REQUEST** | Client | Broadcast | "I accept this IP" / "Renew this IP" |
| **ACK** | Server | Broadcast/Unicast | "It's yours, confirmed" |
| **NAK** | Server | Broadcast | "No! That IP is no longer available" |
| **DECLINE** | Client | Broadcast | "This IP is already in use" |
| **RELEASE** | Client | Unicast | "I'm done with this IP" |
| **INFORM** | Client | Unicast | "I already have IP, just need config" |

### 3.7 DHCP Relay Agent

By default, DHCP uses broadcasts — which **don't cross router boundaries**. If DHCP server is on a different subnet:

```
Without Relay Agent:
  Client (192.168.1.x) broadcasts DISCOVER
  Router BLOCKS broadcast → DHCP server on different subnet never sees it!

With DHCP Relay Agent (configured on router):
  Client broadcasts DISCOVER
  Router's relay agent intercepts, converts to UNICAST
  Sends to DHCP server at known IP (10.0.0.100) ✅
  DHCP server responds to relay agent
  Relay agent forwards back to client
```

### 3.8 DHCP IP Pool and Static Assignment

```
DHCP Pool:
  Network:       192.168.1.0/24
  Range:         192.168.1.100 – 192.168.1.200   ← dynamic pool
  Reserved:      192.168.1.1   (router/gateway)
  Excluded:      192.168.1.1 – 192.168.1.99       ← static devices

DHCP Reservation (Static DHCP / MAC binding):
  MAC: AA:BB:CC:DD:EE:FF → Always gets 192.168.1.150
  (Server, printer, NAS — devices that need stable IPs)
```

---

## 4. Protocol Quick-Reference Table

| Protocol | Port | Transport | Model | Use Case | Secure Version |
|---------|------|-----------|-------|---------|----------------|
| **FTP** | 20/21 | TCP | Client-Server | File transfer | SFTP (22), FTPS (990) |
| **SMTP** | 25/587 | TCP | Client-Server | Sending email | SMTPS (465) |
| **POP3** | 110 | TCP | Client-Server | Download email | POP3S (995) |
| **IMAP** | 143 | TCP | Client-Server | Sync email | IMAPS (993) |
| **DHCP** | 67/68 | UDP | Client-Server | Auto IP config | — |
| **DNS** | 53 | UDP/TCP | Client-Server | Name resolution | DoH, DoT |
| **HTTP** | 80 | TCP | Client-Server | Web browsing | HTTPS (443) |
| **SSH** | 22 | TCP | Client-Server | Secure remote shell | (itself secure) |

---

## 5. Interview Questions

### FTP
**Q1: Why does FTP use two connections?**
> FTP separates control (commands/responses) from data to allow commands to be sent while data is transferring, and to maintain control even after a data transfer completes. Control on port 21 persists; data on port 20 is created per transfer.

**Q2: What is the difference between Active and Passive FTP?**
> In Active mode, the server initiates the data connection to the client — problematic if the client has a firewall. In Passive mode, the server provides a port and the client initiates the data connection — firewall-friendly and the modern default.

**Q3: Why is FTP insecure and what are the alternatives?**
> FTP transmits credentials and data in plain text. Alternatives: SFTP (FTP-like interface over SSH, port 22), FTPS (FTP with TLS encryption).

### SMTP
**Q4: What is the difference between SMTP, POP3, and IMAP?**
> SMTP sends email (client to server, or server to server). POP3 downloads email from server to client and typically deletes the server copy. IMAP synchronizes email between server and client, keeping messages on the server — better for multi-device access.

**Q5: Walk through how an email goes from sender to recipient.**
> 1) Sender's email client sends to sender's SMTP server (port 587). 2) Sender's SMTP server does an MX record DNS lookup for recipient's domain. 3) Sender's SMTP server connects to recipient's mail server (port 25). 4) Recipient's mail server stores the message. 5) Recipient's client retrieves via IMAP/POP3.

### DHCP
**Q6: What is the DORA process?**
> DORA = Discover, Offer, Request, Acknowledge. Client broadcasts Discover ("need an IP"). Server broadcasts Offer ("take 192.168.1.100"). Client broadcasts Request ("I accept"). Server broadcasts/unicasts ACK ("confirmed, lease is 24 hours").

**Q7: Why does DHCP use UDP instead of TCP?**
> When a client needs an IP, it has none yet and can't establish a TCP connection. DHCP uses broadcasts (255.255.255.255), which TCP doesn't support. UDP's connectionless, broadcast-compatible nature fits perfectly.

**Q8: What is a DHCP lease and what happens when it expires?**
> A DHCP lease is a time-limited IP address assignment. At 50% of lease duration, the client tries to renew with the same server. At 87.5%, it broadcasts to any server. On expiry, it releases the IP and restarts DORA.

**Q9: What is a DHCP relay agent?**
> A DHCP relay agent (configured on a router) forwards DHCP broadcasts as unicast to a DHCP server on a different subnet. Since broadcasts don't cross router boundaries, the relay agent makes it possible to have a single centralized DHCP server for multiple subnets.

---

*← Back to [Index](./README.md)*
