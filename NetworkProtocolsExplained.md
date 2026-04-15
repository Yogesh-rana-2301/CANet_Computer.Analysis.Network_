# Network Protocols Explained - Placement Notes
  
## 1. IP Explained (Internet Protocol)

### What IP is

- IP means Internet Protocol.
- It is the foundational protocol of the internet.
- Every internet-connected device has an IP address (phone, laptop, server).
- IP address is a numerical label used to identify devices on a network.
- Analogy: home address for a house.
  
### How IP transports data

- IP breaks data into packets.
- Packet header includes:
  - Source IP address
  - Destination IP address
  - TTL (Time To Live): max router hops before packet is dropped
  - Checksum: detects corruption

Analogy from transcript:

- Sending a book by mailing each page in a separate envelope.

### IPv4 and IPv6

- IPv4 uses 32-bit addresses.
- Total IPv4 space: about 4.3 billion addresses.
- IPv4 pool exhaustion reached in 2011 at the global allocation level.
- IPv6 was introduced with 128-bit addresses.
- IPv6 space is approximately 340 undecillion addresses ($3.4 \times 10^{38}$).

### Most important IP property

- IP is connectionless and unreliable by design.
- IP does not guarantee:
  - delivery
  - ordering
  - non-duplication
- IP forwards packets best-effort, then moves on.

## 2. TCP Explained (Reliable Communication)

### Why TCP exists

- TCP (Transmission Control Protocol) fixes reliability gaps left by IP.
- IP can lose, reorder, or duplicate packets.
- For integrity-sensitive systems, this is unacceptable.

### Core TCP mechanisms

- Connection setup (handshake) before data transfer.
- Sequence numbers so receiver can detect missing or out-of-order data.
- Acknowledgements (ACKs) for received segments.
- Retransmission timeout (RTO): sender resends if ACK is not received in time.
- Sliding window flow control: prevents sender from overwhelming receiver.
- Congestion control: reduces sending rate during packet loss/congestion.

### Result

- Ordered, reliable byte stream between endpoints.

### Protocols commonly riding on TCP (as taught)

- HTTP
- HTTPS
- MQTT
- WebSocket

## 3. UDP Explained (Fast and Lightweight)

### What UDP is

- UDP (User Datagram Protocol) is intentionally minimal.
- It is the design opposite of TCP for reliability features.
  
### What UDP removes

- No handshake
- No sequence numbers
- No acknowledgements
- No retransmission
- No flow control
- No congestion control

### UDP header

- Minimal 8-byte header:
  - Source port
  - Destination port
  - Length
  - Checksum
- Compare with TCP minimum 20-byte header.

### Why UDP exists

- Lower latency and lower overhead.
- For real-time applications, stale retransmitted data can be worse than dropped data.

### Typical UDP use cases from transcript

- Live video streaming
- Online gaming
- Voice calls
- DNS lookups

### DNS packet count example from transcript

- DNS over UDP: typically 2 packets (query + response).
- DNS over TCP: minimum around 7 packets.

## 4. DNS Explained (How Domains Work)

### What DNS does

> Nameserver: A nameserver is a specialized server within the Domain Name System (DNS) that acts as the internet's "phone book," translating human-readable domain names (e.g., example.com) into numerical IP addresses (e.g., 192.0.2.1) that computers use to locate websites. They store DNS records, such as A, CNAME, and MX records, directing traffic to the correct web host.

### DNS Resolution Order
- Local Cache (Browser + OS)
  - Browser cache checked first
  - Then OS-level cache (/etc/hosts, DNS cache)
- Recursive Resolver (ISP DNS / Public DNS)
  - If not cached locally, request goes to a resolver (e.g., Google Public DNS or Cloudflare DNS)
- Root Name Server
  - Resolver asks: “Where is .com?”
  - Root servers respond with TLD servers
- TLD (Top-Level Domain) Name Server
  - Example: .com, .org, .in
  - Tells where the authoritative server for example.com is
- Authoritative Name Server
  - Final authority for the domain
  - Returns actual IP address of www.example.com
- Response Returned Back
  - Resolver caches it
  - Sends IP back to your system
  - Browser connects to that IP

# DNS Name Server Hierarchy

## 🌐 1. Root Name Server

### 🔹 What it is
Top-level entry point of DNS hierarchy.

### 🔹 What it stores
- Does NOT store IPs of websites  
- Stores:
  - List of all TLDs (.com, .org, .in, etc.)
  - Pointers (NS records) to TLD name servers  

### 🔹 Example
You ask: `www.google.com`  
Root server says:  
“I don’t know Google, but ask .com servers.”

---

## 🌍 2. TLD (Top-Level Domain) Name Server

### 🔹 What it is
Handles domains under a specific extension (like .com, .in)

### 🔹 What it stores
- Does NOT store final IPs (usually)  
- Stores:
  - Which authoritative name server handles a domain  
  - NS records for domains under it  

### 🔹 Example
You ask .com server: `google.com`  
It says:  
“Go to Google’s authoritative name server.”

---

## 🧠 3. Authoritative Name Server

### 🔹 What it is
Final source of truth for a domain

### 🔹 What it stores
- Actual DNS records:
  - A → domain → IP  
  - AAAA → domain → IPv6  
  - CNAME → alias  
  - MX → mail servers  
  - TXT → verification/security  
  - NS → its own name servers  

### 🔹 Example
You ask: `www.google.com`  
It responds:  
“Here is the IP: 142.250.x.x”

---

## ⚡ Clean Mental Model

| Layer           | Knows About       | Stores                         |
|----------------|------------------|--------------------------------|
| Root           | TLDs             | “Where is .com?”               |
| TLD            | Domains          | “Where is google.com?”         |
| Authoritative  | Specific domain  | “Here is the IP”               |

---

## 🧠 Ultra-Short Analogy

- Root = Phonebook index (which section to go to)  
- TLD = Section (which page/person)  
- Authoritative = Exact contact details


- DNS (Domain Name System) maps domain names to IP addresses.
- Users type names like google.com, not numeric IPs.

### Resolution flow

1. Client asks DNS resolver.
2. Resolver checks cache.
3. If cache miss: resolver queries root servers.
4. Then TLD servers.
5. Then authoritative name server.
6. Resolver returns final IP answer.

### Operational details

- Usually completes very quickly (often under tens of milliseconds for normal cases).
- Default transport is UDP port 53 for standard lookups.

### Security point

- Traditional DNS is unencrypted by default.
- Network providers can observe queried domains.
- DNS over HTTPS (DoH) encrypts DNS queries inside HTTPS traffic.

## 5. HTTP Explained (Web Communication)

### What HTTP is

- HTTP (Hypertext Transfer Protocol) is browser-server application protocol. 


|Layer	|Protocol	|Role|
|----------------|------------------|--------------------------------|
|Application	|HTTP	|Defines request/response (GET, POST)|
|Transport	|TCP	|Ensures reliable delivery|
|Network	|IP	|Handles addressing & routing|

### Model

- Request/response model.
- Common methods taught:
  - GET: fetch resource
  - POST: submit/process data
  - PUT: update resource
  - DELETE: remove resource

### Common status codes taught

- 200: success
- 404: not found
- 500: server error

### Version milestones taught

- HTTP/2 (2015): multiplex multiple requests over one connection.
- HTTP/3 (2022): uses QUIC to reduce latency, especially on mobile and lossy networks.

## 6. HTTPS Explained (Security and Encryption)

### What HTTPS is

- HTTPS is HTTP protected by TLS encryption.

- ## 🔒 What TLS Actually Does

### 1. Encryption
- Converts data into unreadable form  
- Prevents attackers from reading it  

### 2. Integrity
- Ensures data is not modified in transit  

### 3. Authentication
- Verifies the server is genuine (not fake)  

---

## 🧠 How It Works (High-Level Flow)

### Step 1: Handshake
- Client connects to server  
- Server sends certificate (proof of identity)  

### Step 2: Key Exchange
- Both agree on a shared secret key  

### Step 3: Secure Communication
- All further data is encrypted  

---

## 🌐 Example

### Without TLS:
```http
GET /password=1234
```
### Anyone can read this ❌
With TLS:
Encrypted gibberish
### Only server can decrypt ✅
## Key Concept
TLS uses:
Asymmetric encryption (initial handshake)
Symmetric encryption (fast data transfer)

--- 

### Why HTTPS matters

- Without HTTPS, traffic is plain text and can be read if intercepted.
- Sensitive data (passwords, cards, tokens) must be encrypted in transit.

### TLS handshake goals taught

- Authenticate server identity via digital certificate.
- Establish shared session keys securely.
- Encrypt traffic so intermediaries cannot read content.

### Encryption note from transcript

- AES-256 referenced as encryption example.

### Practical note

- HTTPS is baseline requirement for modern web apps handling user data.

## 7. MQTT Explained (IoT Communication)

### What MQTT is

- MQTT = Message Queuing Telemetry Transport.
- Designed for constrained, unreliable, high-latency links.


### Communication model

- Publish/subscribe through a central broker.
- Publishers send messages to topics.
- Subscribers receive only topics they subscribe to.
- End devices do not need direct point-to-point communication with each other.

### Why MQTT scales well in IoT

- Very low protocol overhead.
- Minimal control packet can be as small as 2 bytes.
- Good fit for constrained devices and battery-sensitive networks.

### Typical usage

- Smart home devices
- Industrial sensors
- Telemetry systems

## 8. WebSocket Explained (Real-Time Data)

### Why WebSocket was needed

- HTTP request/response is not ideal for instant server push.
- Polling is inefficient and adds delay.

### Standardization

- WebSocket standardized in RFC 6455 (December 2011).

### How it starts

- Begins with HTTP request including protocol upgrade.
- Server responds with status 101 (Switching Protocols).
- Connection becomes persistent and full-duplex.

### What full-duplex gives you

- Client and server can both send data anytime.
- No repeated polling round trips.
- Better fit for low-latency updates.

### Typical usage

- Live chat
- Trading dashboards
- Multiplayer browser games
- Real-time collaboration tools

## 9. Quick Comparison (Interview Revision)

| Protocol  | Main Goal                      | Reliability         | Typical Port(s)         | Typical Use                   |
| --------- | ------------------------------ | ------------------- | ----------------------- | ----------------------------- |
| IP        | Addressing and routing packets | Best-effort only    | N/A                     | Base internet layer           |
| TCP       | Reliable ordered delivery      | Yes                 | Varies by app           | Web, messaging, critical data |
| UDP       | Low-latency transport          | No                  | Varies by app           | Streaming, gaming, DNS        |
| DNS       | Name to IP resolution          | App-dependent       | 53 (UDP/TCP)            | Domain lookup                 |
| HTTP      | Web request/response           | Via transport       | 80 (common)             | Websites, APIs                |
| HTTPS     | Secure HTTP over TLS           | Via transport + TLS | 443 (common)            | Secure websites, APIs         |
| MQTT      | Lightweight pub/sub messaging  | Usually over TCP    | 1883/8883 (common)      | IoT telemetry                 |
| WebSocket | Persistent real-time channel   | Usually over TCP    | 80/443 via HTTP upgrade | Chat, realtime apps           |

## 10. Placement Prep Prompts

1. Explain why IP is intentionally unreliable and how TCP compensates.
2. Compare TCP and UDP for video calls and justify choice.
3. Walk through DNS resolution from browser to authoritative server.
4. Explain how HTTPS protects against passive interception.
5. Explain when MQTT is better than HTTP for device communication.
6. Explain why WebSocket outperforms polling for live updates.
